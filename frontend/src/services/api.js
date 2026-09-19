import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'X-Atheus-Key': 'dev-key-123',
    'Content-Type': 'application/json'
  }
});

export const simulateBurst = async () => {
  const res = await api.post('/telemetry/simulate/burst');
  return res.data;
};

export const simulateReset = async () => {
  const res = await api.post('/telemetry/simulate/reset');
  return res.data;
};

export const executeContainment = async (payload) => {
  const res = await api.post('/containment/execute', payload);
  return res.data;
};

export const chatCopilot = async (payload) => {
  const res = await api.post('/copilot/chat', payload);
  return res.data;
};
