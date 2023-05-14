document.addEventListener('DOMContentLoaded', () => {
    const salidaInput = document.querySelector('input[name="fecha_salida"]');
    const llegadaInput = document.querySelector('input[name="fecha_llegada"]');
  
    salidaInput.addEventListener('input', () => {
        const salidaValue = new Date(salidaInput.value);
        const llegadaMinValue = new Date(salidaValue.getTime() + 60 * 60 * 1000); // Agregar 1 hora
  
        const llegadaMin = llegadaMinValue.toISOString().slice(0, 16);
        llegadaInput.min = llegadaMin;
    });
  });
  