function setupTable() {
  const rowCount = parseInt(document.getElementById("blast_count").value);
  const useVector2 = document.getElementById("vector2").checked;
  const tbody = document.getElementById("blastTableBody");
  const warningBox = document.getElementById("blast-warning");

  if (rowCount < 2 || rowCount > 50) {
    warningBox.innerText = "⚠️ Lõhkamiste arv peab olema vahemikus 2 kuni 50.";
    warningBox.style.display = "block";
    return;
  } else {
    warningBox.style.display = "none";
  }

  // Salvesta olemasolevad väärtused
  const oldValues = {};
  const inputs = tbody.querySelectorAll("input");
  inputs.forEach(input => {
    oldValues[input.name] = input.value;
  });

  // Puhasta vana tabel
  tbody.innerHTML = "";

  for (let i = 1; i <= rowCount; i++) {
    const row = document.createElement("tr");

    // Nr
    const cellNr = document.createElement("td");
    cellNr.textContent = i;
    row.appendChild(cellNr);

    // Kaugus
    const cellKaugus = document.createElement("td");
    const inputKaugus = createInput(`kaugus_${i}`);
    inputKaugus.value = oldValues[`kaugus_${i}`] || "";
    cellKaugus.appendChild(inputKaugus);
    row.appendChild(cellKaugus);

    // Mass
    const cellMass = document.createElement("td");
    const inputMass = createInput(`mass_${i}`);
    inputMass.value = oldValues[`mass_${i}`] || "";
    cellMass.appendChild(inputMass);
    row.appendChild(cellMass);

    // Vektor 1
    const cellV1 = document.createElement("td");
    const inputV1 = createInput(`vektor1_${i}`);
    inputV1.value = oldValues[`vektor1_${i}`] || "";
    cellV1.appendChild(inputV1);
    row.appendChild(cellV1);

    // Vektor 2
    const cellV2 = document.createElement("td");
    if (useVector2) {
      const inputV2 = createInput(`vektor2_${i}`);
      inputV2.value = oldValues[`vektor2_${i}`] || "";
      cellV2.appendChild(inputV2);
    } else {
      cellV2.textContent = "—";
    }
    row.appendChild(cellV2);

    tbody.appendChild(row);
  }

  document.getElementById("calculation-area").style.display = "block";
}

function createInput(name) {
  const input = document.createElement("input");
  input.name = name;
  input.type = "number";
  input.step = "any";
  input.required = true;
  input.classList.add("reg-input");
  return input;
}
