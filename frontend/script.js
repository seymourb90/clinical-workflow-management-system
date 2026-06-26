const API_URL = "http://127.0.0.1:5000";

document.getElementById("visitForm").addEventListener("submit", async function(event) {
  event.preventDefault();

  const visit = {
    first_name: document.getElementById("firstName").value,
    last_name: document.getElementById("lastName").value,
    date_of_birth: document.getElementById("dob").value,
    phone_number: document.getElementById("phone").value,
    department: document.getElementById("department").value,
    provider: document.getElementById("provider").value
  };

  await fetch(`${API_URL}/visits`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(visit)
  });

  document.getElementById("visitForm").reset();
  loadVisits();
});

async function loadVisits() {
  const response = await fetch(`${API_URL}/visits`);
  const visits = await response.json();

  const table = document.getElementById("visitTable");
  table.innerHTML = "";

  visits.forEach(visit => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${visit.first_name} ${visit.last_name}</td>
      <td>${visit.department}</td>
      <td>${visit.provider}</td>
      <td>${visit.status}</td>
      <td>${visit.check_in_time}</td>
      <td>
        <select onchange="updateStatus(${visit.visit_id}, this.value)">
          <option value="">Select Status</option>
          <option value="Nurse Assessment">Nurse Assessment</option>
          <option value="Provider Visit">Provider Visit</option>
          <option value="Orders Pending">Orders Pending</option>
          <option value="Discharged">Discharged</option>
        </select>
      </td>
    `;

    table.appendChild(row);
  });
}

async function updateStatus(visitId, status) {
  if (!status) return;

  await fetch(`${API_URL}/visits/${visitId}/status`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ status })
  });

  loadVisits();
}

loadVisits();