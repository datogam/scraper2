// custom javascript

$(document).ready(() => {
  console.log('Sanity Check!');
  setInterval(function() {
    getTasks();
  }, 5000);
});

$('.button').on('click', function() {
  $.ajax({
    url: '/task/',
    data: { type: $(this).data('type') },
    method: 'POST',
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.task_id}</td>
        <td>${res.status}</td>
        <td>${res.created}</td>
      </tr>
    `;
    $('#tasks').prepend(html);
  })
  .fail((err) => {
    console.log(err);
  });
});

function getTasks() {
  $.ajax({
    url: '/tasks/',
    method: 'POST',
  })
  .done((res) => {
    var html;
    for (var i = 0; i < res.tasks.length; i++) {
      html += `
        <tr>
          <td>${res.tasks[i].fields.task_id}</td>
          <td>${res.tasks[i].fields.status}</td>
          <td>${res.tasks[i].fields.created}</td>
        </tr>
      `;
    }
    $('#tasks').html(html);
  })
  .fail((err) => {
    console.log(err);
  })
}
