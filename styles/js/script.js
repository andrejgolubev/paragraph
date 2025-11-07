document.addEventListener('DOMContentLoaded', function() {
  const selectElement = document.querySelector('select');
  const customSelect = document.querySelector('.custom-select');

  const updateSelectStyles = () => {
    customSelect.classList.toggle('select-valid', selectElement.value !== "");
  };
  selectElement.addEventListener('change', updateSelectStyles);
});