document.getElementById('sort-button').addEventListener('click', function() {
   const items = document.querySelectorAll('.property-item');
   
   items.forEach(item => {
       if (item.getAttribute('data-sale') === 'true') {
           item.style.display = 'list-item'; // Показываем карточки для продажи
       } else {
           item.style.display = 'none'; // Скрываем остальные карточки
       }
   });
});
