import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../pages/index';

test('renders home title', () => {
  render(<Home />);
  const el = screen.getByText(/AI Companion/i);
  expect(el).toBeInTheDocument();
});
