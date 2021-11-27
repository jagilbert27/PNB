function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteStudent(student_id) {

  // alert(student_id)

  fetch("/delete-student", {
    method: "POST",
    body: JSON.stringify({ student_id: student_id }),
  }).then((_res) => {
    window.location.href = "/students";
  });

}
