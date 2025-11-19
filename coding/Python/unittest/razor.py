@router.post("/razorpay-webhook")
async def razorpay_webhook(request: Request):
    """
    Receives Razorpay webhooks and verifies signatures securely.
    """
    # Read raw request body
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8").strip()  # strip newline/spaces
    print("\n🔔 [WEBHOOK RECEIVED]")
    print("📦 Raw body:", repr(body_str))

    # Read headers
    signature = request.headers.get("x-razorpay-signature")
    secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")

    print(f"🧩 Header Signature: {signature}")
    print(f"🔑 Loaded Secret: {secret}")

    if not secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    # Verify signature
    verified = False
    expected = None
    try:
        # Try Razorpay SDK verification
        razorpay_client.utility.verify_webhook_signature(body_str, signature, secret)
        verified = True
        print("✅ Verified using Razorpay SDK")
    except Exception as e:
        # Manual fallback verification
        expected = hmac.new(secret.encode(), body_str.encode(), hashlib.sha256).hexdigest()
        verified = (expected == signature)
        print(f"🧮 Fallback verification: expected={expected}\n✅ Match: {verified}")

    if not verified:
        print("❌ Signature verification failed!")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid webhook signature. Debug info: Expected={expected}, Received={signature}"
        )
    else:
        print("✅ Webhook signature verified successfully!")

    # Parse JSON event
    try:
        event = json.loads(body_str)
        event_type = event.get("event")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON body: {e}")

    print(f"📢 Event type: {event_type}")

    # Extract subscription ID
    sub_id = (
        event.get("payload", {}).get("subscription", {}).get("entity", {}).get("id")
        or event.get("payload", {}).get("payment", {}).get("entity", {}).get("subscription_id")
    )
    print(f"🆔 Subscription ID: {sub_id}")

    # Process event
    if sub_id:
        try:
            print(f"🔄 Processing subscription {sub_id} for event {event_type}")
            if event_type in ("subscription.activated", "subscription.charged", "payment.captured"):
                print(f"   Activating subscription {sub_id}...")
                result = await payment_service.update_subscription_status(sub_id, "active", extend_expiry=True)
                print(f"✅ Subscription {sub_id} activated (result: {bool(result)})")
            elif event_type == "subscription.cancelled":
                print(f"   Cancelling subscription {sub_id}...")
                await payment_service.update_subscription_status(sub_id, "cancelled")
                print(f"✅ Subscription {sub_id} cancelled successfully")
        except Exception as e:
            print(f"❌ ERROR updating subscription {sub_id}: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️ No subscription ID found in webhook payload.")

    print("🏁 Webhook processed successfully.\n")
    return {"status": "ok"}