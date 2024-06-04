import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import CustomSubmitButtom from "../components/CustomSubmitButtom";

function CustomModal(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Header>
      <Modal.Body>

      <CustomSubmitButtom/>
      </Modal.Body>

    </Modal>
  );
}

export default CustomModal;
