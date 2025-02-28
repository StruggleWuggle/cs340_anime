document.addEventListener("DOMContentLoaded", function() {
    const addBtn = document.getElementById("addBtn");
    const editBtns = document.querySelectorAll(".edit-btn");
    const modal = document.getElementById("editModal");
    const form = document.getElementById("editForm");
    const closeModal = document.createElement("span");

    closeModal.innerHTML = "&times;";
    closeModal.classList.add("close");
    document.querySelector(".modal-content").prepend(closeModal);

    // open modal
    function openModal() {
        modal.style.display = "block";
    }

    function closeModalFunc() {
        modal.style.display = "none";
        form.reset();
        document.getElementById("entryId").value = "";
    }

    addBtn.addEventListener("click", function () {
        openModal();
    });

    editBtns.forEach(button => {
        button.addEventListener("click", function () {
            let rowData = JSON.parse(this.getAttribute("data-row"));
            document.getElementById("entryId").value = rowData.id;

            Object.keys(rowData).forEach(key => {
                if (document.getElementById(key)) {
                    document.getElementById(key).value = rowData[key];
                }
            });

            openModal();
        });
    });

    closeModal.addEventListener("click", closeModalFunc);

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModalFunc();
        }
    });
});