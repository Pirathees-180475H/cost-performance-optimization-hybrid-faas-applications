import React from 'react';

const Card = ({ type, onClose, children }) => {
  const cardStyle = {
    backgroundColor: '#ffebee',
    border: '1px solid #e53935',
    borderRadius: '4px',
    padding: '10px',
    marginBottom: '10px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    color: '#e53935',
    position: 'relative',
  };

  const closeButtonStyle = {
    position: 'absolute',
    top: '5px',
    right: '5px',
    cursor: 'pointer',
    color: '#e53935',
  };

  const errorIconStyle = {
    marginRight: '5px',
  };

  return (
    <div style={cardStyle}>
      {type === 'error' && (
        <div>
          <i className="bx bxs-error-circle" style={errorIconStyle}></i>
          {children}
        </div>
      )}

      <i className="bx bx-x" style={closeButtonStyle} onClick={onClose}></i>
    </div>
  );
};

export default Card;
