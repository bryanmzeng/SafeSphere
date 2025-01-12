// components/HousingList.js
import React from 'react';
import { Link } from 'react-router-dom';

function HousingItem({ item }) {
  return (
    <Link to={`/item/${item.id}`} className="housing-item">
      <img src={item.image} alt={item.title} />
      <h3>{item.title}</h3>
      <p>{item.price}</p>
      <p>{item.distance}</p>
    </Link>
  );
}

function HousingList({ items }) {
  return (
    <div className="housing-list">
      {items.map(item => (
        <HousingItem key={item.id} item={item} />
      ))}
    </div>
  );
}

export default HousingList;
