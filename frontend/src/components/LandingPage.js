import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';

const collegeOptions = [
  { value: 'harvard', label: 'Harvard University' },
  { value: 'mit', label: 'Massachusetts Institute of Technology' },
  { value: 'stanford', label: 'Stanford University' },
  { value: 'caltech', label: 'California Institute of Technology' }
];

function LandingPage() {
  const [selectedCollege, setSelectedCollege] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (selectedCollege) {
      navigate(`/main?college=${selectedCollege.value}`);
    }
  };

  return (
    <div className="landing-page">
      <div className="oxide-container">
        <h1 className="oxide-title">College Housing Finder</h1>
        <div className="select-container">
          <Select
            options={collegeOptions}
            onChange={setSelectedCollege}
            placeholder="Select a college..."
          />
        </div>
        <button 
          onClick={handleSubmit} 
          className="oxide-button"
          disabled={!selectedCollege}
        >
          Find Housing
        </button>
      </div>
    </div>
  );
}

export default LandingPage;
