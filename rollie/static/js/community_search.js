document.getElementById("searchInput").addEventListener("keyup", function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll("#communityTable tbody tr");
    rows.forEach(row => {
        const nameCell = row.cells[1].innerText.toLowerCase();
        row.style.display = nameCell.includes(filter) ? "" : "none";
    });
});