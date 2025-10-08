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
        
        // Export results button
        const exportBtn = document.getElementById('exportResultsBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportResults();
            });
        }

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
        
        // Load results when switching to results tab
        if (tabId === 'results') {
            this.loadPreviousResults();
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
                    
                    // Check if message is JSON (validation_complete event)
                    if (message.startsWith('{')) {
                        try {
                            const data = JSON.parse(message);
                            if (data.type === 'validation_complete') {
                                this.appendToOutput(`[INFO] ✅ Validación completada. Cambiando a pestaña de resultados...`);
                                console.log('Validation complete, switching to results tab.');
                                
                                // Wait a moment then switch to results and load them
                                setTimeout(() => {
                                    this.switchTab('results');
                                    this.loadPreviousResults();
                                }, 1000);
                                return;
                            }
                        } catch (e) {
                            // Not JSON, treat as regular log message
                            console.warn('Failed to parse WebSocket message as JSON:', message);
                        }
                    }
                    
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
        
        // Tab switching is now handled by WebSocket validation_complete event
        // No longer auto-switching to results tab here
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
                    <td colspan="7" class="text-center text-muted py-4">
                        <i class="bi bi-inbox display-6 d-block mb-2"></i>
                        No hay validaciones disponibles
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = results.map(result => {
            // Extract data from the new format
            const timestamp = result.timestamp || 'N/A';
            const request = result.request || {};
            const resultData = result.result || {};
            const filename = result.filename || '';
            
            const deviceIp = request.ip_address || 'N/A';
            const deviceType = request.device_type || 'N/A';
            const serialNumber = request.serial_number || 'N/A';
            const scenario = request.hostname || deviceType;
            const overallStatus = resultData.overall_status || 'UNKNOWN';
            const stats = resultData.statistics || {};
            const duration = resultData.total_duration_ms ? `${resultData.total_duration_ms}ms` : 'N/A';
            
            const isSuccess = overallStatus === 'PASS';
            const statusClass = isSuccess ? 'success' : 'error';
            const statusText = isSuccess ? 'Exitoso' : 'Falló';
            const statusIcon = isSuccess ? 'check-circle-fill' : 'x-circle-fill';
            
            return `
                <tr>
                    <td>${new Date(timestamp).toLocaleString()}</td>
                    <td>${deviceIp}</td>
                    <td><span class="badge bg-secondary">${serialNumber}</span></td>
                    <td>${scenario}</td>
                    <td>
                        <span class="status-indicator status-${statusClass}">
                            <i class="bi bi-${statusIcon}"></i>
                            ${statusText} (${stats.passed || 0}/${stats.total_commands || 0})
                        </span>
                    </td>
                    <td>${duration}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="drsUI.viewResult('${filename}')">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="drsUI.downloadResult('${filename}')">
                            <i class="bi bi-download"></i>
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    }

    async viewResult(resultId) {
        try {
            const response = await fetch(`/api/results/${resultId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            
            // Show result detail within the results section
            this.showResultDetail(result);
        } catch (error) {
            console.error('Error loading result:', error);
            this.showToast('error', `Error al cargar el resultado: ${error.message}`);
        }
    }
    
    showResultDetail(data) {
        // Hide the results list and show the detail view
        document.getElementById('resultsListView').style.display = 'none';
        document.getElementById('resultDetailView').style.display = 'block';
        
        // Get the detail content container
        const contentDiv = document.getElementById('resultDetailContent');
        
        const result = data.result || data;
        const request = data.request || {};
        const stats = result.statistics || {};
        
        // Build the detail view HTML
        const detailHTML = `
            <!-- Overview Section -->
            <div class="result-detail-section mb-4">
                <h5><i class="bi bi-info-circle"></i> Información General</h5>
                <div class="row">
                    <div class="col-md-3">
                        <div class="result-stat-box">
                            <div class="stat-value">
                                <span class="result-status-badge ${result.overall_status === 'PASS' ? 'pass' : 'fail'}">
                                    <i class="bi bi-${result.overall_status === 'PASS' ? 'check-circle-fill' : 'x-circle-fill'}"></i>
                                    ${result.overall_status || 'UNKNOWN'}
                                </span>
                            </div>
                            <div class="stat-label">Estado General</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="result-stat-box">
                            <div class="stat-value">${stats.total_commands || 0}</div>
                            <div class="stat-label">Total Comandos</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="result-stat-box">
                            <div class="stat-value">${stats.passed || 0}</div>
                            <div class="stat-label">Exitosos</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="result-stat-box">
                            <div class="stat-value">${stats.success_rate || 0}%</div>
                            <div class="stat-label">Tasa de Éxito</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Device Information -->
            <div class="result-detail-section mb-4">
                <h5><i class="bi bi-hdd-network"></i> Información del Dispositivo</h5>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Dirección IP:</strong> ${request.ip_address || 'N/A'}</p>
                        <p><strong>Tipo de Dispositivo:</strong> ${request.device_type || 'N/A'}</p>
                        <p><strong>Número de Serie:</strong> ${request.serial_number || 'N/A'}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Modo:</strong> ${request.live_mode ? 'Live' : 'Mock'}</p>
                        <p><strong>Fecha y Hora:</strong> ${new Date(data.timestamp).toLocaleString('es-ES')}</p>
                        <p><strong>Duración Total:</strong> ${result.total_duration_ms ? `${result.total_duration_ms} ms` : 'N/A'}</p>
                    </div>
                </div>
            </div>

            <!-- Command Results -->
            <div class="result-detail-section">
                <h5><i class="bi bi-list-check"></i> Resultados de Comandos</h5>
                <div id="commandResults">
                    ${this.renderCommandResults(result.results || [])}
                </div>
            </div>
        `;
        
        contentDiv.innerHTML = detailHTML;
        
        // Add event listener for back button
        document.getElementById('backToResultsBtn').addEventListener('click', () => {
            this.showResultsList();
        });
    }
    
    renderCommandResults(commands) {
        if (commands.length === 0) {
            return '<p class="text-muted">No hay resultados de comandos disponibles.</p>';
        }

        return commands.map((cmd, index) => {
            const status = cmd.status || 'UNKNOWN';
            const isPassed = status === 'PASS';
            
            return `
                <div class="result-command-row ${isPassed ? 'pass' : 'fail'}">
                    <div class="result-command-header">
                        <span class="result-command-name">${index + 1}. ${cmd.command || 'Unknown Command'}</span>
                        <span class="badge bg-${isPassed ? 'success' : 'danger'}">
                            <i class="bi bi-${isPassed ? 'check-circle' : 'x-circle'}"></i>
                            ${status}
                        </span>
                    </div>
                    
                    ${cmd.frame_hex ? `
                        <div>
                            <strong>Trama Hex:</strong>
                            <div class="result-code-block">${cmd.frame_hex}</div>
                        </div>
                    ` : ''}
                    
                    ${cmd.response_hex ? `
                        <div>
                            <strong>Respuesta Hex:</strong>
                            <div class="result-code-block">${cmd.response_hex}</div>
                        </div>
                    ` : ''}
                    
                    ${cmd.decoded_values ? `
                        <div>
                            <strong>Valores Decodificados:</strong>
                            <div class="result-code-block">${JSON.stringify(cmd.decoded_values, null, 2)}</div>
                        </div>
                    ` : ''}
                    
                    ${cmd.details ? `
                        <div>
                            <strong>Detalles:</strong>
                            <div class="result-code-block">${cmd.details}</div>
                        </div>
                    ` : ''}
                    
                    ${cmd.duration_ms ? `
                        <div>
                            <small class="text-muted">
                                <i class="bi bi-clock"></i> Duración: ${cmd.duration_ms} ms
                            </small>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
    }
    
    showResultsList() {
        // Show the results list and hide the detail view
        document.getElementById('resultsListView').style.display = 'block';
        document.getElementById('resultDetailView').style.display = 'none';
    }
    
    showResultModal(data) {
        // Create modal content with the result data
        const resultData = data.result || data;
        const request = data.request || {};
        
        const modalHTML = `
            <div class="modal fade" id="resultModal" tabindex="-1">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">📊 Resultado de Validación</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <h6>Información del Dispositivo</h6>
                                    <p><strong>IP:</strong> ${request.ip_address || 'N/A'}</p>
                                    <p><strong>Tipo:</strong> ${request.device_type || 'N/A'}</p>
                                    <p><strong>Serial:</strong> ${request.serial_number || 'N/A'}</p>
                                    <p><strong>Modo:</strong> ${request.live_mode ? 'Live' : 'Mock'}</p>
                                </div>
                                <div class="col-md-6">
                                    <h6>Estadísticas</h6>
                                    <p><strong>Estado:</strong> <span class="badge bg-${resultData.overall_status === 'PASS' ? 'success' : 'danger'}">${resultData.overall_status}</span></p>
                                    <p><strong>Comandos:</strong> ${resultData.statistics?.passed}/${resultData.statistics?.total_commands}</p>
                                    <p><strong>Duración:</strong> ${resultData.duration_ms}ms</p>
                                    <p><strong>Tasa de Éxito:</strong> ${resultData.statistics?.success_rate}%</p>
                                </div>
                            </div>
                            <h6>Resultados de Comandos</h6>
                            <div class="table-responsive" style="max-height: 400px; overflow-y: auto;">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Comando</th>
                                            <th>Estado</th>
                                            <th>Trama</th>
                                            <th>Respuesta</th>
                                            <th>Duración</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${resultData.results?.map(r => `
                                            <tr>
                                                <td>${r.command}</td>
                                                <td><span class="badge bg-${r.status === 'PASS' ? 'success' : 'danger'}">${r.status}</span></td>
                                                <td><code>${r.details}</code></td>
                                                <td><code>${r.response_data?.substring(0, 50)}...</code></td>
                                                <td>${r.duration_ms}ms</td>
                                            </tr>
                                        `).join('') || '<tr><td colspan="5">No hay resultados</td></tr>'}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if any
        const existingModal = document.getElementById('resultModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Show modal using Bootstrap
        const modal = new bootstrap.Modal(document.getElementById('resultModal'));
        modal.show();
    }

    async downloadResult(resultId) {
        try {
            const response = await fetch(`/api/results/${resultId}/download`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
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
            this.showToast('info', 'Exportando resultados...');
            
            const response = await fetch('/api/results/export/csv');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const blob = await response.blob();
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            // Get filename from Content-Disposition header if available
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = `drs_validation_results_${new Date().toISOString().split('T')[0]}.csv`;
            
            if (contentDisposition) {
                const matches = /filename=([^;]+)/.exec(contentDisposition);
                if (matches && matches[1]) {
                    filename = matches[1].trim();
                }
            }
            
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            this.showToast('success', 'Resultados exportados exitosamente');
        } catch (error) {
            console.error('Error exporting results:', error);
            this.showToast('error', `Error al exportar resultados: ${error.message}`);
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