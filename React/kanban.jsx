import React, { useState, useRef, useEffect } from 'react';
import { 
  Plus, 
  MoreVertical, 
  X, 
  Edit3, 
  Trash2, 
  ArrowLeft, 
  ArrowRight,
  Save,
  Calendar,
  User,
  Tag,
  CheckSquare,
  Search,
  Filter,
  MoreHorizontal,
  List,
  Layout,
  Users,
  FileText,
  Clock,
  BarChart3,
  Share,
  Maximize2,
  Settings,
  ChevronDown,
  Grid3X3,
  Eye,
  UserCheck,
  AlertCircle
} from 'lucide-react';

import { navItems, priorityColors } from '@/components/kanban/TaskConfig';

import TaskCard from '@/components/kanban/TaskCard';
import TaskForm from '@/components/kanban/TaskForm';
import TaskModal from '@/components/kanban/TaskModal';
import ColumnEditor from '@/components/kanban/ColumnEditor';
import ColumnForm from '@/components/kanban/ColumnForm';
const KanbanDashboard = () => {
  // State Management
  const [columns, setColumns] = useState([
    { 
      id: 1, 
      name: 'IN PROGRESS', 
      color: '#3b82f6',
      count: 1,
      tasks: [
        { 
          id: 1, 
          title: 'Ankit', 
          code: 'KAN-2',
          description: 'Setup project architecture and initial components',
          priority: 'medium',
          dueDate: '2024-08-15',
          assignee: 'Ankit Sharma',
          avatar: 'AS',
          tags: ['Development', 'Setup'],
          status: 'In Progress'
        }
      ]
    },
    { 
      id: 2, 
      name: 'TO DO', 
      color: '#6b7280',
      count: 0,
      tasks: []
    },
    { 
      id: 3, 
      name: 'IN REVIEW', 
      color: '#f59e0b',
      count: 0,
      tasks: []
    },
    { 
      id: 4, 
      name: 'DONE', 
      color: '#10b981',
      count: 0,
      tasks: []
    }
  ]);

  const [activeView, setActiveView] = useState('Board');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterOpen, setFilterOpen] = useState(false);
  const [groupBy, setGroupBy] = useState('Status');
  const [draggedTask, setDraggedTask] = useState(null);
  const [activeMenu, setActiveMenu] = useState(null);
  const [hoveredColumn, setHoveredColumn] = useState(null);
  const [isAddingColumn, setIsAddingColumn] = useState(false);
  const [isAddingTask, setIsAddingTask] = useState(null);
  const [editingColumn, setEditingColumn] = useState(null);
  const [taskModal, setTaskModal] = useState(null);
  const [showMoreMenu, setShowMoreMenu] = useState(false);

  const menuRef = useRef(null);
  const modalRef = useRef(null);
  const filterRef = useRef(null);



  // Column Management
  const addColumn = (name, color = '#6b7280') => {
    const newColumn = {
      id: Date.now(),
      name: name.toUpperCase(),
      color,
      count: 0,
      tasks: []
    };
    setColumns([...columns, newColumn]);
    setIsAddingColumn(false);
  };

  const updateColumn = (columnId, name, color) => {
    setColumns(columns.map(col => 
      col.id === columnId ? { ...col, name: name.toUpperCase(), color } : col
    ));
    setEditingColumn(null);
  };

  const deleteColumn = (columnId) => {
    setColumns(columns.filter(col => col.id !== columnId));
    setActiveMenu(null);
  };

  const moveColumn = (columnId, direction) => {
    const columnIndex = columns.findIndex(col => col.id === columnId);
    if (
      (direction === -1 && columnIndex === 0) ||
      (direction === 1 && columnIndex === columns.length - 1)
    ) return;

    const newColumns = [...columns];
    const [movedColumn] = newColumns.splice(columnIndex, 1);
    newColumns.splice(columnIndex + direction, 0, movedColumn);
    setColumns(newColumns);
    setActiveMenu(null);
  };

  // Task Management
  const addTask = (columnId, taskData) => {
    const newTask = {
      id: Date.now(),
      title: taskData.title,
      code: `KAN-${Date.now().toString().slice(-3)}`,
      description: taskData.description || '',
      priority: taskData.priority || 'medium',
      dueDate: taskData.dueDate || '',
      assignee: taskData.assignee || '',
      avatar: taskData.assignee ? taskData.assignee.split(' ').map(n => n[0]).join('') : '',
      tags: taskData.tags || [],
      status: taskData.status || 'To Do'
    };

    setColumns(columns.map(col => {
      if (col.id === columnId) {
        return { 
          ...col, 
          tasks: [...col.tasks, newTask],
          count: col.tasks.length + 1
        };
      }
      return col;
    }));
    setIsAddingTask(null);
  };

  const updateTask = (taskId, taskData) => {
    setColumns(columns.map(col => ({
      ...col,
      tasks: col.tasks.map(task =>
        task.id === taskId ? { ...task, ...taskData } : task
      )
    })));
    setTaskModal(null);
  };

  const deleteTask = (taskId) => {
    setColumns(columns.map(col => ({
      ...col,
      tasks: col.tasks.filter(task => task.id !== taskId),
      count: col.tasks.filter(task => task.id !== taskId).length
    })));
    setTaskModal(null);
  };

  // Drag and Drop for Tasks
  const handleTaskDragStart = (e, task, fromColumnId) => {
    setDraggedTask({ task, fromColumnId });
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleTaskDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleTaskDrop = (e, toColumnId) => {
    e.preventDefault();
    if (!draggedTask) return;

    const { task, fromColumnId } = draggedTask;
    if (fromColumnId === toColumnId) return;

    setColumns(columns.map(col => {
      if (col.id === fromColumnId) {
        return { 
          ...col, 
          tasks: col.tasks.filter(t => t.id !== task.id),
          count: col.tasks.filter(t => t.id !== task.id).length
        };
      }
      if (col.id === toColumnId) {
        return { 
          ...col, 
          tasks: [...col.tasks, task],
          count: col.tasks.length + 1
        };
      }
      return col;
    }));

    setDraggedTask(null);
  };

  // Event Listeners
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setActiveMenu(null);
      }
      if (modalRef.current && !modalRef.current.contains(e.target)) {
        setTaskModal(null);
      }
      if (filterRef.current && !filterRef.current.contains(e.target)) {
        setFilterOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        {/* Top Header */}
        <div className="px-6 py-3 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-sm text-gray-600">Projects</div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center">
                  <Layout className="w-4 h-4 text-white" />
                </div>
                <h1 className="text-lg font-semibold text-gray-900">My Kanban Project</h1>
                <button className="p-1 hover:bg-gray-100 rounded">
                  <MoreHorizontal className="w-4 h-4 text-gray-500" />
                </button>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button className="p-2 hover:bg-gray-100 rounded-lg">
                <Maximize2 className="w-4 h-4 text-gray-600" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded-lg">
                <Share className="w-4 h-4 text-gray-600" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded-lg">
                <Settings className="w-4 h-4 text-gray-600" />
              </button>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="px-6 py-0">
          <div className="flex items-center gap-6">
            {navItems.map((item) => (
              <button
                key={item.name}
                onClick={() => setActiveView(item.name)}
                className={`flex items-center gap-2 px-3 py-3 text-sm font-medium border-b-2 transition-colors ${
                  item.name === activeView
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                <item.icon className="w-4 h-4" />
                {item.name}
              </button>
            ))}
            <button className="flex items-center justify-center w-8 h-8 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded">
              <Plus className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Controls */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search board"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* User Avatar */}
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  AM
                </div>
              </div>

              {/* Filter */}
              <div className="relative" ref={filterRef}>
                <button
                  onClick={() => setFilterOpen(!filterOpen)}
                  className="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-lg text-sm hover:bg-gray-50"
                >
                  <Filter className="w-4 h-4" />
                  Filter
                </button>
                {filterOpen && (
                  <div className="absolute top-full left-0 mt-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                    <div className="p-4">
                      <h3 className="font-medium text-gray-900 mb-3">Filter Options</h3>
                      <div className="space-y-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Assignee</label>
                          <select className="w-full border border-gray-300 rounded px-3 py-2 text-sm">
                            <option>All users</option>
                            <option>Ankit Sharma</option>
                          </select>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                          <select className="w-full border border-gray-300 rounded px-3 py-2 text-sm">
                            <option>All priorities</option>
                            <option>High</option>
                            <option>Medium</option>
                            <option>Low</option>
                          </select>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                          <select className="w-full border border-gray-300 rounded px-3 py-2 text-sm">
                            <option>All statuses</option>
                            <option>In Progress</option>
                            <option>To Do</option>
                            <option>In Review</option>
                            <option>Done</option>
                          </select>
                        </div>
                      </div>
                      <div className="flex gap-2 mt-4">
                        <button className="flex-1 bg-blue-600 text-white py-2 px-4 rounded text-sm hover:bg-blue-700">
                          Apply
                        </button>
                        <button 
                          onClick={() => setFilterOpen(false)}
                          className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded text-sm"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center gap-4">
              {/* Group By */}
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Group</span>
                <button className="flex items-center gap-1 px-3 py-2 border border-gray-300 rounded-lg text-sm hover:bg-gray-50">
                  {groupBy}
                  <ChevronDown className="w-4 h-4" />
                </button>
              </div>

              {/* View Options */}
              <div className="flex items-center gap-1 border border-gray-300 rounded-lg p-1">
                <button className="p-1.5 rounded text-gray-600 hover:bg-gray-100">
                  <Grid3X3 className="w-4 h-4" />
                </button>
                <button className="p-1.5 rounded text-gray-600 hover:bg-gray-100">
                  <Eye className="w-4 h-4" />
                </button>
              </div>

              {/* More Options */}
              <button className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
                <MoreHorizontal className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Kanban Board */}
      <div className="p-6">
        <div className="flex gap-6 overflow-x-auto">
          {/* Columns */}
          {columns.map((column, index) => (
            <div
              key={column.id}
              className="flex-shrink-0 w-80"
            >
              {/* Column Header */}
              <div
                className="mb-4"
                onMouseEnter={() => setHoveredColumn(column.id)}
                onMouseLeave={() => setHoveredColumn(null)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {editingColumn === column.id ? (
                      <ColumnEditor
                        column={column}
                        onSave={updateColumn}
                        onCancel={() => setEditingColumn(null)}
                      />
                    ) : (
                      <>
                        <h3 className="font-semibold text-gray-700 text-sm tracking-wide">
                          {column.name}
                        </h3>
                        <span className="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded-full font-medium">
                          {column.count}
                        </span>
                        {column.name === 'DONE' && (
                          <CheckSquare className="w-4 h-4 text-green-600" />
                        )}
                      </>
                    )}
                  </div>

                  {/* Column Menu */}
                  <div className="relative">
                    <button
                      onClick={() => setActiveMenu(activeMenu === column.id ? null : column.id)}
                      className={`p-1 rounded hover:bg-gray-100 transition-all duration-200 ${
                        hoveredColumn === column.id || activeMenu === column.id
                          ? 'opacity-100 visible'
                          : 'opacity-0 invisible'
                      }`}
                    >
                      <MoreVertical className="w-4 h-4 text-gray-500" />
                    </button>

                    {activeMenu === column.id && (
                      <div ref={menuRef} className="absolute right-0 top-8 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                        <button
                          onClick={() => setEditingColumn(column.id)}
                          className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm hover:bg-gray-50 text-gray-700"
                        >
                          <Edit3 className="w-4 h-4" />
                          Edit Column
                        </button>
                        {index > 0 && (
                          <button
                            onClick={() => moveColumn(column.id, -1)}
                            className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm hover:bg-gray-50 text-gray-700"
                          >
                            <ArrowLeft className="w-4 h-4" />
                            Move Left
                          </button>
                        )}
                        {index < columns.length - 1 && (
                          <button
                            onClick={() => moveColumn(column.id, 1)}
                            className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm hover:bg-gray-50 text-gray-700"
                          >
                            <ArrowRight className="w-4 h-4" />
                            Move Right
                          </button>
                        )}
                        <button
                          onClick={() => deleteColumn(column.id)}
                          className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm hover:bg-gray-50 text-red-600"
                        >
                          <Trash2 className="w-4 h-4" />
                          Delete Column
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Tasks Container */}
              <div
                className="min-h-[400px] bg-gray-100 rounded-lg p-3"
                onDragOver={handleTaskDragOver}
                onDrop={(e) => handleTaskDrop(e, column.id)}
              >
                <div className="space-y-3">
                  {column.tasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onDragStart={(e) => handleTaskDragStart(e, task, column.id)}
                      onClick={() => setTaskModal(task)}
                      priorityColors={priorityColors}
                    />
                  ))}

                  {/* Add Task Button */}
                  {isAddingTask === column.id ? (
                    <TaskForm
                      onSubmit={(taskData) => addTask(column.id, taskData)}
                      onCancel={() => setIsAddingTask(null)}
                    />
                  ) : (
                    <button
                      onClick={() => setIsAddingTask(column.id)}
                      className="w-full p-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-600 transition-colors duration-200 flex items-center justify-center gap-2"
                    >
                      <Plus className="w-4 h-4" />
                      Create
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}

          {/* Add Column */}
          <div className="flex-shrink-0 w-80">
            {isAddingColumn ? (
              <ColumnForm
                onSubmit={addColumn}
                onCancel={() => setIsAddingColumn(false)}
              />
            ) : (
              <button
                onClick={() => setIsAddingColumn(true)}
                className="w-full h-32 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-600 transition-colors duration-200 flex items-center justify-center gap-2 mt-12"
              >
                <Plus className="w-4 h-4" />
                Add Column
              </button>
            )}
          </div>

          {/* Add New Item Button */}
          <div className="flex-shrink-0 w-12 mt-12">
            <button className="w-10 h-10 bg-gray-200 rounded-lg flex items-center justify-center text-gray-600 hover:bg-gray-300 transition-colors">
              <Plus className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Task Modal */}
      {taskModal && (
        <TaskModal
          task={taskModal}
          onUpdate={updateTask}
          onDelete={deleteTask}
          onClose={() => setTaskModal(null)}
          priorityColors={priorityColors}
          modalRef={modalRef}
        />
      )}
    </div>
  );
};



export default KanbanDashboard;