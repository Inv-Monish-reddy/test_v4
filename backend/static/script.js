/**
 * Animation Calculator - Frontend JavaScript
 * Handles form submission, API calls, and animations
 */

// DOM Elements
const calcForm = document.getElementById('calcForm');
const num1Input = document.getElementById('num1');
const num2Input = document.getElementById('num2');
const operatorSelect = document.getElementById('operator');
const resultContainer = document.getElementById('resultContainer');
const resultValue = document.getElementById('resultValue');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');

/**
 * Hide both result and error containers with animation
 */
function hideAll() {
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
}

/**
 * Show result with animation
 * @param {number} result - The calculated result
 */
function showResult(result) {
    // Hide error first
    errorContainer.classList.add('hidden');
    
    // Update result value
    resultValue.textContent = result;
    
    // Show result with animation
    resultContainer.classList.remove('hidden');
    resultContainer.classList.add('fade-in');
}

/**
 * Show error message with animation
 * @param {string} message - Error message to display
 */
function showError(message) {
    // Hide result first
    resultContainer.classList.add('hidden');
    
    // Update error message
    errorMessage.textContent = message;
    
    // Show error with animation
    errorContainer.classList.remove('hidden');
    errorContainer.classList.add('shake');
}

/**
 * Make API call to /calculate endpoint
 * @param {number} num1 - First number
 * @param {number} num2 - Second number
 * @param {string} operator - Operation to perform
 */
async function calculate(num1, num2, operator) {
    try {
        // Prepare request payload
        const payload = {
            num1: num1,
            num2: num2,
            operator: operator
        };

        // Make POST request to Flask backend
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        // Parse response
        const data = await response.json();

        // Handle response based on status code
        if (response.ok) {
            // Success - show result
            showResult(data.result);
        } else {
            // Error - show error message
            const errorMsg = data.error || 'An unknown error occurred';
            showError(errorMsg);
        }
    } catch (error) {
        // Network or other errors
        console.error('Calculation error:', error);
        showError('Network error: Could not connect to server');
    }
}

/**
 * Handle form submission
 */
calcForm.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent default form submission
    
    // Get form values
    const num1 = parseFloat(num1Input.value);
    const num2 = parseFloat(num2Input.value);
    const operator = operatorSelect.value;

    // Validate input
    if (isNaN(num1) || isNaN(num2)) {
        showError('Please enter valid numbers');
        return;
    }

    // Hide previous results/errors
    hideAll();

    // Perform calculation
    calculate(num1, num2, operator);
});

/**
 * Clear results when user starts typing
 */
function addInputListeners() {
    const inputs = [num1Input, num2Input, operatorSelect];
    
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            // Optionally clear previous results
            // hideAll();
        });
    });
}

// Initialize
addInputListeners();
