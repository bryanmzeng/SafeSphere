// components/MainPage.js
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Select from 'react-select';
import HousingList from './HousingList';

const filterOptions = [
  { value: 'distance', label: 'Distance' },
  { value: 'price', label: 'Price' },
];

function MainPage() {
  const [filter, setFilter] = useState({ value: 'distance', label: 'Distance' });
  const [housingItems, setHousingItems] = useState([]);
  const location = useLocation();

  useEffect(() => {
    // Fetch housing items based on the selected college and filter
    // Update setHousingItems with the fetched data
  }, [location.search, filter]);

  return (
    <div className="main-page">
      <h1>Housing Options</h1>
      <Select
        options={filterOptions}
        value={filter}
        onChange={setFilter}
      />
      <HousingList items={housingItems} />
    </div>
  );
}

export default MainPage;
