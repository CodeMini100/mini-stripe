import React, { useState } from 'react';
import axios from 'axios';

/**
 * App.js
 *
 * The main application component that demonstrates interactions with
 * Flask endpoints for creating charges, processing refunds, and more.
 * In a production environment, set REACT_APP_API_BASE_URL in your .env file
 * to ensure secure deployment.
 */
function App() {
  /**
   * API base URL defined via environment variable, falling back to localhost for development.
   * @constant
   * @type {string}
   */
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

  /**
   * State for form data related to creating a charge.
   * @type {[{amount: string, description: string}, Function]}
   */
  const [chargeData, setChargeData] = useState({ amount: '', description: '' });

  /**
   * State for form data related to creating a refund.
   * @type {[{chargeId: string}, Function]}
   */
  const [refundData, setRefundData] = useState({ chargeId: '' });

  /**
   * State for displaying status messages (success or error).
   * @type {[string, Function]}
   */
  const [statusMessage, setStatusMessage] = useState('');

  /**
   * handleChargeDataChange
   * Handles change events for the charge creation form fields.
   * @param {Object} e - The event object from the input field.
   */
  const handleChargeDataChange = (e) => {
    const { name, value } = e.target;
    setChargeData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  /**
   * handleRefundDataChange
   * Handles change events for the refund form field.
   * @param {Object} e - The event object from the input field.
   */
  const handleRefundDataChange = (e) => {
    const { name, value } = e.target;
    setRefundData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  /**
   * handleCreateCharge
   * Sends a POST request to create a new charge.
   * @async
   * @function
   */
  const handleCreateCharge = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/create_charge`, chargeData);
      setStatusMessage(`Charge created successfully: ${response.data.id}`);
    } catch (error) {
      setStatusMessage(`Error creating charge: ${error.response ? error.response.data : error.message}`);
    }
  };

  /**
   * handleCreateRefund
   * Sends a POST request to create a new refund for an existing charge.
   * @async
   * @function
   */
  const handleCreateRefund = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/create_refund`, refundData);
      setStatusMessage(`Refund created successfully: ${response.data.id}`);
    } catch (error) {
      setStatusMessage(`Error creating refund: ${error.response ? error.response.data : error.message}`);
    }
  };

  return (
    <div style={{ margin: '2rem' }}>
      <h1>Stripe Integration Demo</h1>

      <section style={{ marginBottom: '2rem' }}>
        <h2>Create Charge</h2>
        <label>
          Amount:
          <input
            type="text"
            name="amount"
            value={chargeData.amount}
            onChange={handleChargeDataChange}
          />
        </label>
        <label>
          Description:
          <input
            type="text"
            name="description"
            value={chargeData.description}
            onChange={handleChargeDataChange}
          />
        </label>
        <button onClick={handleCreateCharge}>Create Charge</button>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2>Refund Charge</h2>
        <label>
          Charge ID:
          <input
            type="text"
            name="chargeId"
            value={refundData.chargeId}
            onChange={handleRefundDataChange}
          />
        </label>
        <button onClick={handleCreateRefund}>Create Refund</button>
      </section>

      {statusMessage && <p>{statusMessage}</p>}
    </div>
  );
}

export default App;