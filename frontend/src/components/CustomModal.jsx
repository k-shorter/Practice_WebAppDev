import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import CustomSubmitButtom from "../components/CustomSubmitButtom";

const CustomModal = ({ show, onHide, children }) => {
  if (!show) {
    return null;
  }

  return (
    <div className="modal">
      <div className="modal-content">
        <span className="close-button" onClick={onHide}>&times;</span>
        {children}
      </div>
    </div>
  );
};

export default CustomModal;
