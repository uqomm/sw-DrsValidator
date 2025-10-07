/* Modern JavaScript for DRS Validator UI */
/* Bootstrap 5 Integration + Enhanced User Experience */
/* Version: 2.0 - October 2025 */

class DRSValidatorUI {
    constructor() {
        this.currentTab = 'validation';
        this.validationInProgress = false;
        this.sidebarOpen = window.innerWidth >= 768;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupSidebar();
        this.setupFormValidation();
        this.setupToastNotifications();
        this.loadPreviousResults();
        this.loadSavedConfiguration(); // Load saved device configuration
        
        // Ensure validation tab is visible by default
        this.switchTab('validation');
        
        // Force device config panel visibility
        setTimeout(() => {
            const configPanel = document.getElementById('deviceConfigPanel');
            const rightColumn = document.querySelector('.col-xl-4');
            const validationTab = document.getElementById('validation');
            
            if (configPanel) {
                configPanel.style.display = 'block';
                configPanel.style.visibility = 'visible';
                configPanel.style.opacity = '1';
            }
            if (rightColumn) {
                rightColumn.style.display = 'block';
                rightColumn.style.visibility = 'visible';
            }
            if (validationTab) {
                validationTab.style.display = 'block';
                const rows = validationTab.querySelectorAll('.row');
                rows.forEach(row => {
                    row.style.display = 'flex';
                });
            }
        }, 100);
        
        console.log('DRS Validator UI v2.0 initialized');
    }

    /* ========================================
       EVENT LISTENERS
    ======================================== */
    setupEventListeners() {
        // Sidebar toggle
        document.getElementById('sidebarToggle').addEventListener('click', () => {
            this.toggleSidebar();
        });

        // Form submission
        document.getElementById('validationForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startValidation();
        });

        // Tab navigation
        document.querySelectorAll('[data-tab]').forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                const tabId = e.currentTarget.dataset.tab;
                this.switchTab(tabId);
            });
        });

        // Device configuration buttons
        document.getElementById('testConnectionBtn').addEventListener('click', () => {
            this.testDeviceConnection();
        });

        document.getElementById('saveConfigBtn').addEventListener('click', () => {
            this.saveDeviceConfiguration();
        });

        // Window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // Mobile overlay click to close sidebar
        document.addEventListener('click', (e) => {
            if (window.innerWidth < 768 && 
                this.sidebarOpen && 
                !e.target.closest('.sidebar') && 
                !e.target.closest('.sidebar-toggle') &&
                document.body.classList.contains('sidebar-open')) {
                this.sidebarOpen = false;
                this.updateSidebarState();
            }
        });
    }

    /* ========================================
       SIDEBAR MANAGEMENT
    ======================================== */
    setupSidebar() {
        // Initialize sidebar state based on screen size
        if (window.innerWidth >= 768) {
            this.sidebarOpen = true;
        } else {
            this.sidebarOpen = false;
        }
        this.updateSidebarState();
    }

    toggleSidebar() {
        this.sidebarOpen = !this.sidebarOpen;
        this.updateSidebarState();
    }

    updateSidebarState() {
        const sidebar = document.getElementById('sidebar');
        const body = document.body;
        
        if (this.sidebarOpen) {
            sidebar.classList.add('active');
            // Add class to body for mobile overlay
            if (window.innerWidth < 768) {
                body.classList.add('sidebar-open');
            }
        } else {
            sidebar.classList.remove('active');
            body.classList.remove('sidebar-open');
        }
        
        // Dispatch a custom event to notify other components of the change
        window.dispatchEvent(new Event('sidebar:toggle'));
    }

    handleResize() {
        const body = document.body;
        
        if (window.innerWidth >= 768) {
            this.sidebarOpen = true;
            // Remove mobile overlay class when switching to desktop
            body.classList.remove('sidebar-open');
        } else {
            this.sidebarOpen = false;
        }
        this.updateSidebarState();
    }

    /* ========================================
       TAB NAVIGATION
    ======================================== */
    switchTab(tabId) {
        // Update active nav item in the sidebar
        document.querySelectorAll('.sidebar-nav-item').forEach(item => {
            item.classList.remove('active');
        });
        const navItem = document.querySelector(`[data-tab="${tabId}"]`);
        if (navItem) {
            navItem.classList.add('active');
        }

        // Hide all tab content and then show the correct one using an 'active' class
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        const tabContent = document.getElementById(tabId);
        if (tabContent) {
            tabContent.classList.add('active');
        }
        
        // Ensure device configuration panel is visible in validation tab
        if (tabId === 'validation') {
            const configPanel = document.getElementById('deviceConfigPanel');
            if (configPanel) {
                configPanel.style.display = 'block';
                configPanel.style.visibility = 'visible';
            }
        }

        // Update breadcrumb
        const currentPage = document.getElementById('currentPage');
        if (currentPage) {
            const tabNames = {
                'validation': 'Validación',
                'results': 'Resultados',
                'batch': 'Comandos Batch',
                'monitoring': 'Monitoreo',
                'help': 'Ayuda'
            };
            currentPage.textContent = tabNames[tabId] || 'DRS Validator';
        }
        
        this.currentTab = tabId;
        
        // Close sidebar on mobile after navigation
        if (window.innerWidth < 768) {
            this.sidebarOpen = false;
            this.updateSidebarState();
        }
    }

    /* ========================================
       FORM VALIDATION & SUBMISSION
    ======================================== */
    setupFormValidation() {
        const form = document.getElementById('validationForm');
        if (!form) return;

        // Real-time IP validation
        const deviceIp = document.getElementById('deviceIp');
        if (deviceIp) {
            deviceIp.addEventListener('input', (e) => {
                this.validateIPAddress(e.target);
            });
        }

        // Port validation
        const devicePort = document.getElementById('devicePort');
        if (devicePort) {
            devicePort.addEventListener('input', (e) => {
                this.validatePort(e.target);
            });
        }
    }

    validateIPAddress(input) {
        const ipPattern = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
        const isValid = ipPattern.test(input.value);
        
        if (input.value && !isValid) {
            input.classList.add('is-invalid');
            this.showFieldError(input, 'Formato de IP inválido');
        } else {
            input.classList.remove('is-invalid');
            this.hideFieldError(input);
        }
        
        return isValid;
    }

    validatePort(input) {
        const port = parseInt(input.value);
        const isValid = port >= 1 && port <= 65535;
        
        if (input.value && !isValid) {
            input.classList.add('is-invalid');
            this.showFieldError(input, 'Puerto debe estar entre 1 y 65535');
        } else {
            input.classList.remove('is-invalid');
            this.hideFieldError(input);
        }
        
        return isValid;
    }

    showFieldError(input, message) {
        let errorDiv = input.nextElementSibling;
        if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            input.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }

    hideFieldError(input) {
        const errorDiv = input.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
            errorDiv.remove();
        }
    }

    /* ========================================
       VALIDATION PROCESS
    ======================================== */

    async startValidation() {
        if (this.validationInProgress) {
            this.showToast('warning', 'Validación ya en progreso');
            return;
        }

        const formData = new FormData(document.getElementById('validationForm'));
        const validationData = Object.fromEntries(formData);

        // Validate required fields
        if (!this.validateForm(validationData)) {
            return;
        }

        this.validationInProgress = true;
        this.showValidationProgress();
        this.clearOutput();
        
        const startBtn = document.getElementById('startValidationBtn');
        this.setButtonLoading(startBtn, true);

        try {
            await this.executeValidation(validationData);
        } catch (error) {
            this.showToast('error', 'Error durante la validación');
            console.error('Validation error:', error);
        } finally {
            this.validationInProgress = false;
            this.setButtonLoading(startBtn, false);
        }
    }

    validateForm(data) {
        const requiredFields = ['scenario_id', 'ip_address', 'port', 'timeout'];
        const missingFields = requiredFields.filter(field => !data[field]);
        
        if (missingFields.length > 0) {
            this.showToast('error', 'Por favor complete todos los campos requeridos');
            return false;
        }

        // Validate IP format
        const ipInput = document.getElementById('deviceIp');
        if (!this.validateIPAddress(ipInput)) {
            this.showToast('error', 'Formato de IP inválido');
            return false;
        }

        // Validate port range
        const portInput = document.getElementById('devicePort');
        if (!this.validatePort(portInput)) {
            this.showToast('error', 'Puerto inválido');
            return false;
        }

        return true;
    }

    async executeValidation(validationData) {
        try {
            // Step 1: Start validation task
            const response = await fetch('/api/validation/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...validationData,
                    use_websockets: true  // Enable new WebSocket functionality
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            
            // Check if this is the new WebSocket response or legacy response
            if (result.client_id && result.status === 'started') {
                // New WebSocket approach
                const clientId = result.client_id;
                this.appendToOutput(`[INFO] 🚀 Iniciando validación con ID: ${clientId}`);
                
                // Step 2: Connect to WebSocket for real-time logs
                await this.connectToValidationLogs(clientId);
            } else {
                // Legacy approach - handle direct response
                this.handleLegacyValidationResponse(result);
            }

        } catch (error) {
            this.appendToOutput(`[ERROR] ❌ Error al ejecutar validación: ${error.message}`);
            throw error;
        }
    }

    handleLegacyValidationResponse(result) {
        // Handle the new BatchCommandsValidator response format
        this.appendToOutput(`[INFO] 📊 Estado General: ${result.overall_status || result.status}`);
        this.appendToOutput(`[INFO] 💬 ${result.message}`);
        
        // Show command type and mode
        if (result.command_type) {
            this.appendToOutput(`[INFO] 🔧 Tipo de Comandos: ${result.command_type.toUpperCase()}`);
        }
        if (result.mode) {
            this.appendToOutput(`[INFO] 🎮 Modo: ${result.mode.toUpperCase()}`);
        }
        
        // Show statistics
        if (result.statistics) {
            const stats = result.statistics;
            this.appendToOutput(`[STATS] 📈 Total: ${stats.total_commands} | ✅ Exitosos: ${stats.passed} | ❌ Fallidos: ${stats.failed} | ⏱️ Timeouts: ${stats.timeouts}`);
            this.appendToOutput(`[STATS] 🎯 Tasa de Éxito: ${stats.success_rate}% | ⏰ Promedio: ${stats.average_duration_ms}ms`);
        }
        
        // Show individual test results with hex frames and decoded values
        if (result.tests && result.tests.length > 0) {
            this.appendToOutput(`\n[COMMANDS] 📋 Comandos Ejecutados:`);
            result.tests.forEach((test, index) => {
                const status = test.status === 'PASS' ? '✅' : test.status === 'TIMEOUT' ? '⏱️' : '❌';
                const commandType = test.is_set_command ? 'SET' : 'GET';
                const typeIcon = test.is_set_command ? '⚙️' : '🔍';
                
                // Main command line
                this.appendToOutput(`\n[${index + 1}] ${status} ${typeIcon} ${commandType} Command: ${test.name}`);
                this.appendToOutput(`    📝 ${test.message}`);
                
                // Show hex frames (sent and received)
                if (test.details) {
                    // Try to extract hex frame from details
                    const hexMatch = test.details.match(/trama: ([0-9A-F]+)/i);
                    if (hexMatch) {
                        this.appendToOutput(`    📤 Trama enviada: ${hexMatch[1]}`);
                    }
                }
                
                if (test.response_data) {
                    this.appendToOutput(`    📥 Trama recibida: ${test.response_data}`);
                }
                
                // For SET commands, show configuration confirmation
                if (test.is_set_command && test.status === 'PASS') {
                    this.appendToOutput(`    ✓ Configuración aplicada correctamente`);
                }
                
                // Show decoded values if available (only for GET commands)
                if (!test.is_set_command && test.decoded_values && Object.keys(test.decoded_values).length > 0) {
                    this.appendToOutput(`    🔍 Valores Decodificados:`);
                    for (const [key, value] of Object.entries(test.decoded_values)) {
                        if (key !== 'status' && key !== 'mock_source' && key !== 'raw_bytes' && key !== 'decoder_mapping') {
                            this.appendToOutput(`       • ${key}: ${JSON.stringify(value)}`);
                        }
                    }
                }
                
                if (test.duration_ms) {
                    this.appendToOutput(`    ⏱️ Duración: ${test.duration_ms}ms`);
                }
            });
        }
        
        this.setProgress(100);
        this.updateProgressText('Validación completada');
        this.completeValidation();
    }

    async connectToValidationLogs(clientId) {
        return new Promise((resolve, reject) => {
            try {
                // Determine WebSocket protocol based on current page protocol
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/logs/${clientId}`;
                
                this.appendToOutput(`[INFO] 📡 Conectando a logs en tiempo real...`);
                
                const ws = new WebSocket(wsUrl);
                let logEnded = false;

                ws.onopen = () => {
                    this.appendToOutput(`[INFO] ✅ Conexión WebSocket establecida`);
                };

                ws.onmessage = (event) => {
                    const message = event.data;
                    
                    if (message === '---END_OF_LOG---') {
                        logEnded = true;
                        this.appendToOutput(`[INFO] 📄 Log completado`);
                        ws.close();
                        
                        // Get final result
                        this.getFinalValidationResult(clientId).then(resolve).catch(reject);
                        return;
                    }
                    
                    // Display real-time log message
                    this.appendToOutput(message);
                    this.updateProgressFromLog(message);
                };

                ws.onerror = (error) => {
                    this.appendToOutput(`[ERROR] ❌ Error en WebSocket: ${error}`);
                    reject(new Error('WebSocket connection failed'));
                };

                ws.onclose = (event) => {
                    if (!logEnded) {
                        this.appendToOutput(`[WARNING] ⚠️ Conexión WebSocket cerrada inesperadamente`);
                    }
                };

                // Set timeout for WebSocket connection
                setTimeout(() => {
                    if (!logEnded) {
                        ws.close();
                        reject(new Error('Validation timeout'));
                    }
                }, 30000); // 30 second timeout

            } catch (error) {
                reject(error);
            }
        });
    }

    async getFinalValidationResult(clientId) {
        try {
            const response = await fetch(`/api/validation/task/${clientId}`);
            if (!response.ok) {
                throw new Error('Failed to get validation result');
            }
            
            const result = await response.json();
            this.appendToOutput(`[FINAL] 🎯 Resultado: ${result.status} - ${result.message}`);
            
            return result;
        } catch (error) {
            this.appendToOutput(`[ERROR] ❌ Error obteniendo resultado final: ${error.message}`);
            throw error;
        }
    }

    updateProgressFromLog(logMessage) {
        // Extract progress information from log messages
        if (logMessage.includes('[INFO]') && logMessage.includes('Iniciando')) {
            this.setProgress(10);
            this.updateProgressText('Iniciando validación...');
        } else if (logMessage.includes('Conectando')) {
            this.setProgress(25);
            this.updateProgressText('Estableciendo conexión...');
        } else if (logMessage.includes('Enviando comando')) {
            this.setProgress(50);
            this.updateProgressText('Enviando comandos...');
        } else if (logMessage.includes('Recibida respuesta')) {
            this.setProgress(75);
            this.updateProgressText('Procesando respuesta...');
        } else if (logMessage.includes('[SUCCESS]') || logMessage.includes('completada')) {
            this.setProgress(100);
            this.updateProgressText('Validación completada');
        } else if (logMessage.includes('[ERROR]')) {
            this.updateProgressText('Error en validación');
        }
    }

    completeValidation() {
        this.setProgress(100);
        this.updateProgressText('Validación completada');
        this.showToast('success', 'Validación completada exitosamente');
        
        // Auto-switch to results tab after completion
        setTimeout(() => {
            this.switchTab('results');
            this.loadPreviousResults();
        }, 2000);
    }

    /* ========================================
       UI UPDATES
    ======================================== */
    showValidationProgress() {
        const progressSection = document.getElementById('validationProgress');
        const outputSection = document.getElementById('liveOutputSection');
        
        progressSection.style.display = 'block';
        outputSection.style.display = 'block';
        
        this.setProgress(0);
        this.updateProgressText('Iniciando validación...');
    }

    setProgress(percentage) {
        const progressBar = document.getElementById('progressBar');
        const progressPercent = document.getElementById('progressPercent');
        
        if (progressBar) progressBar.style.width = `${percentage}%`;
        if (progressPercent) progressPercent.textContent = `${percentage}%`;
    }

    updateProgressText(text) {
        const progressText = document.getElementById('progressText');
        if (progressText) progressText.textContent = text;
    }

    appendToOutput(text) {
        const output = document.getElementById('liveOutput');
        if (!output) return;
        
        const line = document.createElement('div');
        line.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
        
        // Color coding based on content
        if (text.includes('ERROR') || text.includes('FAILED')) {
            line.className = 'text-danger';
        } else if (text.includes('SUCCESS') || text.includes('OK')) {
            line.className = 'text-success';
        } else if (text.includes('WARNING')) {
            line.className = 'text-warning';
        } else {
            line.className = 'text-info';
        }
        
        output.appendChild(line);
        output.scrollTop = output.scrollHeight;
    }

    clearOutput() {
        const output = document.getElementById('liveOutput');
        if (output) {
            output.innerHTML = `
                <div class="text-success">DRS Validator v2.0 - Ready</div>
                <div class="text-muted">Esperando comandos...</div>
            `;
        }
    }

    setButtonLoading(button, loading) {
        if (!button) return;
        
        if (loading) {
            button.classList.add('btn-loading');
            button.disabled = true;
        } else {
            button.classList.remove('btn-loading');
            button.disabled = false;
        }
    }

    /* ========================================
       TOAST NOTIFICATIONS
    ======================================== */
    setupToastNotifications() {
        // Create toast container if it doesn't exist
        if (!document.getElementById('toastContainer')) {
            const container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
    }

    showToast(type, message, duration = 5000) {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = 'toast-modern';
        
        const icons = {
            success: 'bi-check-circle-fill text-success',
            error: 'bi-x-circle-fill text-danger',
            warning: 'bi-exclamation-triangle-fill text-warning',
            info: 'bi-info-circle-fill text-info'
        };

        toast.innerHTML = `
            <i class="bi ${icons[type] || icons.info}"></i>
            <div class="flex-grow-1">
                <div class="font-medium">${this.capitalizeFirst(type)}</div>
                <div class="text-sm text-muted">${message}</div>
            </div>
            <button type="button" class="btn-close btn-sm" aria-label="Close"></button>
        `;

        container.appendChild(toast);

        // Add close functionality
        const closeBtn = toast.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => {
            this.removeToast(toast);
        });

        // Auto-remove after duration
        setTimeout(() => {
            this.removeToast(toast);
        }, duration);
    }

    removeToast(toast) {
        toast.style.animation = 'slideOut 0.3s ease-out forwards';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    /* ========================================
       RESULTS MANAGEMENT
    ======================================== */
    async loadPreviousResults() {
        try {
            const response = await fetch('/api/results');
            const data = await response.json();
            
            // Extract the actual results array from the API response
            const results = data.results || [];
            this.updateResultsTable(results);
        } catch (error) {
            console.error('Error loading results:', error);
            this.updateResultsTable([]);
        }
    }

    updateResultsTable(results) {
        const tbody = document.getElementById('resultsTableBody');
        if (!tbody) return;

        if (!results || results.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-muted py-4">
                        <i class="bi bi-inbox display-6 d-block mb-2"></i>
                        No hay validaciones disponibles
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = results.map(result => `
            <tr>
                <td>${new Date(result.timestamp).toLocaleString()}</td>
                <td>${result.device_ip}:${result.port}</td>
                <td>${result.scenario}</td>
                <td>
                    <span class="status-indicator status-${result.status === 'success' ? 'success' : 'error'}">
                        <i class="bi bi-circle-fill"></i>
                        ${result.status === 'success' ? 'Exitoso' : 'Falló'}
                    </span>
                </td>
                <td>${result.duration || 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="drsUI.viewResult('${result.id}')">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="drsUI.downloadResult('${result.id}')">
                        <i class="bi bi-download"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    async viewResult(resultId) {
        try {
            const response = await fetch(`/api/results/${resultId}`);
            const result = await response.json();
            
            // Show result in modal or new tab
            this.showResultModal(result);
        } catch (error) {
            this.showToast('error', 'Error al cargar el resultado');
        }
    }

    async downloadResult(resultId) {
        try {
            const response = await fetch(`/api/results/${resultId}/download`);
            const blob = await response.blob();
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `validation_${resultId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            this.showToast('error', 'Error al descargar el resultado');
        }
    }

    async exportResults() {
        try {
            const response = await fetch('/api/results/export');
            const blob = await response.blob();
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `drs_validation_results_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            this.showToast('success', 'Resultados exportados exitosamente');
        } catch (error) {
            this.showToast('error', 'Error al exportar resultados');
        }
    }

    /* ========================================
       BATCH OPERATIONS
    ======================================== */
    async uploadBatchFile() {
        const fileInput = document.getElementById('batchFile');
        if (!fileInput.files[0]) {
            this.showToast('warning', 'Por favor seleccione un archivo');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        const btn = document.getElementById('uploadBatchBtn');
        this.setButtonLoading(btn, true);

        try {
            const response = await fetch('/api/batch/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('success', 'Archivo batch cargado y ejecutado');
                this.switchTab('validation');
            } else {
                this.showToast('error', `Error: ${result.error}`);
            }
        } catch (error) {
            this.showToast('error', 'Error al cargar archivo batch');
        } finally {
            this.setButtonLoading(btn, false);
        }
    }

    /* ========================================
       KEYBOARD SHORTCUTS
    ======================================== */
    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + Key combinations
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case '1':
                    e.preventDefault();
                    this.switchTab('validation');
                    break;
                case '2':
                    e.preventDefault();
                    this.switchTab('results');
                    break;
                case '3':
                    e.preventDefault();
                    this.switchTab('batch');
                    break;
                case 'b':
                    e.preventDefault();
                    this.toggleSidebar();
                    break;
            }
        }
        
        // Escape key
        if (e.key === 'Escape') {
            if (window.innerWidth < 768 && this.sidebarOpen) {
                this.sidebarOpen = false;
                this.updateSidebarState();
            }
        }
    }

    /* ========================================
       UTILITY METHODS
    ======================================== */
    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /* ========================================
       DEVICE CONFIGURATION PANEL METHODS
    ======================================== */
    async testDeviceConnection() {
        const ipInput = document.getElementById('deviceIp');
        const portInput = document.getElementById('devicePort');
        
        if (!ipInput.value) {
            this.showToast('warning', 'Por favor ingrese una dirección IP');
            return;
        }

        const testBtn = document.getElementById('testConnectionBtn');
        this.setButtonLoading(testBtn, true);

        try {
            // Get the selected mode
            const selectedMode = document.querySelector('input[name="mode"]:checked').value;
            
            const response = await fetch(`/api/validation/ping/${ipInput.value}?mode=${selectedMode}`, {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.status === 'PASS') {
                this.showToast('success', `✅ Conexión exitosa a ${ipInput.value}`);
                this.updateConnectionStatus('connected', `Conectado a ${ipInput.value}:${portInput.value}`);
            } else {
                this.showToast('error', `❌ No se pudo conectar a ${ipInput.value}`);
                this.updateConnectionStatus('disconnected', 'Conexión fallida');
            }
        } catch (error) {
            this.showToast('error', 'Error al probar la conexión');
            this.updateConnectionStatus('error', 'Error de conexión');
        } finally {
            this.setButtonLoading(testBtn, false);
        }
    }

    saveDeviceConfiguration() {
        const deviceConfig = {
            ip_address: document.getElementById('deviceIp').value,
            port: document.getElementById('devicePort').value,
            timeout: document.getElementById('timeout').value,
            timestamp: new Date().toISOString()
        };

        if (!deviceConfig.ip_address) {
            this.showToast('warning', 'Por favor configure una dirección IP');
            return;
        }

        // Save to localStorage
        localStorage.setItem('drs_device_config', JSON.stringify(deviceConfig));
        this.showToast('success', '💾 Configuración guardada exitosamente');
    }

    updateConnectionStatus(status, message) {
        const alertDiv = document.querySelector('.alert');
        if (!alertDiv) return;

        // Remove existing status classes
        alertDiv.classList.remove('alert-info', 'alert-success', 'alert-danger');
        
        const iconSpan = alertDiv.querySelector('i');
        const textDiv = alertDiv.querySelector('div');

        switch (status) {
            case 'connected':
                alertDiv.classList.add('alert-success');
                iconSpan.className = 'bi bi-check-circle-fill me-2';
                textDiv.innerHTML = `<strong>Estado:</strong> Conectado<br><small>${message}</small>`;
                break;
            case 'disconnected':
                alertDiv.classList.add('alert-info');
                iconSpan.className = 'bi bi-info-circle-fill me-2';
                textDiv.innerHTML = `<strong>Estado:</strong> Desconectado<br><small>${message}</small>`;
                break;
            case 'error':
                alertDiv.classList.add('alert-danger');
                iconSpan.className = 'bi bi-exclamation-triangle-fill me-2';
                textDiv.innerHTML = `<strong>Estado:</strong> Error<br><small>${message}</small>`;
                break;
        }
    }

    loadSavedConfiguration() {
        const saved = localStorage.getItem('drs_device_config');
        if (saved) {
            try {
                const config = JSON.parse(saved);
                document.getElementById('deviceIp').value = config.ip_address || '';
                document.getElementById('devicePort').value = config.port || '502';
                document.getElementById('timeout').value = config.timeout || '10';
                
                this.showToast('info', '📋 Configuración cargada desde memoria');
            } catch (error) {
                console.warn('Could not load saved configuration:', error);
            }
        }
    }
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize the UI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.drsUI = new DRSValidatorUI();
});

// Export for global access
window.DRSValidatorUI = DRSValidatorUI;