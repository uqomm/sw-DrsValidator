// DRS Validation Framework - JavaScript Frontend

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupTabNavigation();
    setupValidationForm();
    setupBatchCommandsForm();
}

// Format validation results into HTML
function formatValidationResults(result) {
    const data = result.result || result;

    if (!data || !data.tests) {
        return `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    }

    let html = `<div class="validation-summary-compact">`;

    data.tests.forEach(test => {
        const statusClass = test.status?.toLowerCase() || 'unknown';
        const statusIcon = test.status === 'PASS' ? '✅' : test.status === 'FAIL' ? '❌' : '⚠️';
        
        // Extract hex frame and decoded values if available
        const hexFrame = test.hex_frame || '';
        const decodedValues = test.decoded_values || {};
        const hasDecodedData = Object.keys(decodedValues).length > 0;

        html += `
            <div class="test-item-compact test-${statusClass}">
                <div class="test-compact-header">
                    <span class="test-compact-icon">${statusIcon}</span>
                    <span class="test-compact-name">${test.name}</span>
                    <span class="test-compact-status status-${statusClass}">${test.status}</span>
                </div>
                <div class="test-compact-details">
                    <div class="test-compact-message">${test.message}</div>
                    ${test.details ? `<div class="test-compact-detail-text">${test.details}</div>` : ''}
                    ${test.duration_ms ? `<div class="test-compact-duration">⏱️ ${test.duration_ms}ms</div>` : ''}
                    ${hasDecodedData ? `<div class="test-compact-decoded">
                        <strong>Valores decodificados:</strong>
                        <pre>${JSON.stringify(decodedValues, null, 2)}</pre>
                    </div>` : ''}
                </div>
            </div>
        `;
    });

    html += `
        <div class="validation-summary-footer">
            <div class="overall-status-compact status-${data.overall_status?.toLowerCase() || 'unknown'}">
                Estado General: ${data.overall_status || 'UNKNOWN'}
            </div>
        </div>
    </div>`;

    return html;
}

// Save validation result to history
function saveValidationResult(result, validationData) {
    const historyKey = 'validation_history';
    let history = JSON.parse(localStorage.getItem(historyKey) || '[]');

    const historyItem = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        scenario: result.scenario_name || validationData.scenario_id,
        device_ip: validationData.ip_address,
        device_hostname: validationData.hostname,
        mode: validationData.mode,
        result: result
    };

    // Keep only last 10 results
    history.unshift(historyItem);
    if (history.length > 10) {
        history = history.slice(0, 10);
    }

    localStorage.setItem(historyKey, JSON.stringify(history));

    // Update results tab if it's visible
    updateResultsTab();
}

// Update results tab with history
function updateResultsTab() {
    const resultsTabContent = document.getElementById('resultsHistory');
    if (!resultsTabContent) return;

    const history = JSON.parse(localStorage.getItem('validation_history') || '[]');

    if (history.length === 0) {
        resultsTabContent.innerHTML = `
            <div class="results-empty">
                <h3>📊 Historial de Validaciones</h3>
                <p>No hay resultados guardados aún. Ejecuta una validación para ver los resultados aquí.</p>
            </div>
        `;
        return;
    }

    let html = `
        <div class="results-history">
            <h3>📊 Historial de Validaciones</h3>
            <div class="history-list">
    `;

    history.forEach((item, index) => {
        const date = new Date(item.timestamp).toLocaleString();
        const status = item.result.result?.overall_status || 'UNKNOWN';
        const statusClass = status.toLowerCase();

        html += `
            <div class="history-item" onclick="showValidationDetail(${item.id})">
                <div class="history-header">
                    <div class="history-info">
                        <span class="history-scenario">${item.scenario}</span>
                        <span class="history-device">${item.device_ip}</span>
                        <span class="history-mode">${item.mode}</span>
                    </div>
                    <div class="history-meta">
                        <span class="history-status status-${statusClass}">${status}</span>
                        <span class="history-date">${date}</span>
                    </div>
                </div>
                <div class="history-summary">
                    ${item.result.result?.tests?.length || 0} pruebas ejecutadas
                </div>
            </div>
        `;
    });

    html += `
            </div>
        </div>
    `;

    resultsTabContent.innerHTML = html;
}

// Show detailed validation result
function showValidationDetail(resultId) {
    const history = JSON.parse(localStorage.getItem('validation_history') || '[]');
    const result = history.find(item => item.id === resultId);

    if (!result) return;

    // Create modal or expand the item to show details
    const detailHtml = `
        <div class="validation-detail-modal">
            <div class="modal-header">
                <h3>Detalles de Validación</h3>
                <button onclick="closeValidationDetail()" class="close-btn">×</button>
            </div>
            <div class="modal-content">
                <div class="detail-info">
                    <p><strong>Escenario:</strong> ${result.scenario}</p>
                    <p><strong>Dispositivo:</strong> ${result.device_ip}</p>
                    <p><strong>Modo:</strong> ${result.mode}</p>
                    <p><strong>Fecha:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
                </div>
                <div class="detail-results">
                    ${formatValidationResults(result.result)}
                </div>
            </div>
        </div>
    `;

    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', detailHtml);
}

// Close validation detail modal
function closeValidationDetail() {
    const modal = document.querySelector('.validation-detail-modal');
    if (modal) {
        modal.remove();
    }
}

// Tab Navigation
function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');

            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(tabName).classList.add('active');

            // Update results tab when selected
            if (tabName === 'results') {
                updateResultsTab();
            }
        });
    });
}

// Validation Form Setup
function setupValidationForm() {
    const form = document.getElementById('validationForm');
    const runButton = document.getElementById('runValidationBtn');

    if (form && runButton) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await runValidation();
        });
    }
}

// Run Validation
async function runValidation() {
    const form = document.getElementById('validationForm');
    const runButton = document.getElementById('runValidationBtn');
    const resultsArea = document.getElementById('resultsArea');
    const resultsContainer = document.getElementById('validationResults');

    if (!form||!runButton)return;

    // Validate form
    const scenarioSelect = form.querySelector('#scenarioSelect');
    const deviceIp = form.querySelector('#deviceIp');

    if (!scenarioSelect.value){
        alert('Por favor seleccione un escenario de validación');
        return;
    }

    if (!deviceIp.value){
        alert('Por favor ingrese la dirección IP del dispositivo');
        return;
    }

    // Get form data
    const formData = new FormData(form);
    const validationData = {
        scenario_id: formData.get('scenario_id'),
        ip_address: formData.get('ip_address'),
        port: parseInt(formData.get('port')) || 65050,
        hostname: formData.get('hostname'),
        mode: formData.get('mode')
    };

    // Disable button and show loading
    runButton.disabled = true;
    runButton.textContent = 'Ejecutando...';

    try {
        let result;

        // Check if this is a batch commands scenario
        if (validationData.scenario_id === 'drs_master_batch' || validationData.scenario_id === 'batch_remote_commands') {
            // Execute batch commands instead of regular validation
            result = await runBatchCommandsForValidation(validationData);
        } else {
            // Make regular validation API call
            const response = await fetch('/api/validation/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(validationData),
            });

            if (!response.ok){
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            result = await response.json();
        }

        // Show results area
        if (resultsArea) {
            resultsArea.style.display = 'block';
        }

        // Show results
        if (resultsContainer) {
            resultsContainer.innerHTML = `
                <div class="validation-results-compact">
                    ${formatValidationResults(result)}
                </div>
            `;
        }

        // Save results to history
        saveValidationResult(result, validationData);

    } catch (error) {
        console.error('Error running validation:', error);

        // Show error
        if (resultsContainer) {
            resultsContainer.innerHTML = `
                <div class="alert alert-danger">
                    <h4>❌ Error en la Validación</h4>
                    <p>${error.message || 'Ocurrió un error durante la ejecución de la validación.'}</p>
                </div>
            `;
        }
    } finally {
        // Re-enable button
        runButton.disabled = false;
        runButton.textContent = '🚀 Ejecutar Validación';
    }
}

// Batch Commands Form Setup
function setupBatchCommandsForm() {
    const form = document.getElementById('batchCommandsForm');
    const runButton = document.getElementById('runBatchBtn');

    if (form && runButton) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await runBatchCommands();
        });
    }
}

// Run Batch Commands for Validation Scenario
async function runBatchCommandsForValidation(validationData) {
    // Determine command type based on scenario
    const commandType = validationData.scenario_id === 'batch_remote_commands' ? 'remote' : 'master';
    
    // Prepare batch data
    const batchData = {
        ip_address: validationData.ip_address,
        port: validationData.port || 65050,
        command_type: commandType,
        mode: validationData.mode
    };

    // Make API call to batch commands endpoint
    const response = await fetch('/api/validation/batch-commands', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(batchData),
    });

    if (!response.ok){
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const batchResult = await response.json();

    // Convert batch results to validation format
    return formatBatchResultsAsValidation(batchResult, validationData);
}

// Convert batch command results to validation format
function formatBatchResultsAsValidation(batchResult, validationData) {
    const tests = [];

    if (batchResult.results && Array.isArray(batchResult.results)) {
        batchResult.results.forEach((commandResult, index) => {
            const status = commandResult.success ? 'PASS' : 'FAIL';
            const commandName = commandResult.command || `Comando ${index + 1}`;

            tests.push({
                name: commandName,
                status: status,
                message: commandResult.response || commandResult.message || 'Comando ejecutado',
                details: commandResult.details || null,
                duration_ms: commandResult.duration_ms || null
            });
        });
    }

    // Calculate overall status
    const passedTests = tests.filter(test => test.status === 'PASS').length;
    const totalTests = tests.length;
    const overallStatus = passedTests === totalTests ? 'OK' : (passedTests > 0 ? 'WARNING' : 'CRITICAL');

    return {
        scenario_name: 'DRS Master Batch Commands',
        result: {
            tests: tests,
            overall_status: overallStatus,
            summary: {
                total_commands: totalTests,
                successful_commands: passedTests,
                failed_commands: totalTests - passedTests
            }
        }
    };
}

// Run Batch Commands (original function for batch commands tab)
async function runBatchCommands() {
    const form = document.getElementById('batchCommandsForm');
    const runButton = document.getElementById('runBatchBtn');

    if (!form||!runButton)return;

    // Get form data
    const formData = new FormData(form);
    const batchData = {
        device_ip: formData.get('device_ip'),
        command_type: formData.get('command_type'),
        batch_mode: formData.get('batch_mode') === 'on',
        save_output: formData.get('save_output') === 'on'
    };

    // Disable button and show loading
    runButton.disabled = true;
    runButton.textContent = 'Ejecutando...';

    try {
        // Make API call to backend
        const response = await fetch('/api/validation/batch-commands', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(batchData),
        });

        if (!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Show results
        alert(`✅ Comandos ejecutados exitosamente. Resultados: ${JSON.stringify(result)}`);

    } catch (error) {
        console.error('Error running batch commands:', error);
        alert(`❌ Error al ejecutar comandos: ${error.message}`);
    } finally {
        // Re-enable button
        runButton.disabled = false;
        runButton.textContent = '🚀 Ejecutar Batch';
    }
}
