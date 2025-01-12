// components/ItemDetail.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function ItemDetail() {
  const [item, setItem] = useState(null);
  const [reviews, setReviews] = useState([]);
  const { id } = useParams();

  useEffect(() => {
    // Fetch item details and reviews based on id
    // Update setItem and setReviews with the fetched data
  }, [id]);

  const addReview = (review) => {
    // Implement logic to add a new review
  };

  if (!item) return <div>Loading...</div>;

  return (
    <div className="item-detail">
      <h1>{item.title}</h1>
      <img src={item.image} alt={item.title} />
      <p>{item.description}</p>
      <h2>Reviews</h2>
      {reviews.map(review => (
        <div key={review.id} className="review">
          <p>{review.text}</p>
          <p>Rating: {review.rating}/5</p>
        </div>
      ))}
      {/* Add a form to submit new reviews */}
    </div>
  );
}

export default ItemDetail;
