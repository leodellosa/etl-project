document.addEventListener("DOMContentLoaded", function () {
  const userMenuButton = document.getElementById("user-menu-button");
  const userDropdown = document.getElementById("user-dropdown");

  // Toggle dropdown visibility when the user menu button is clicked
  userMenuButton.addEventListener("click", function (e) {
    e.stopPropagation(); // Prevent the click from propagating to the document
    userDropdown.classList.toggle("hidden");
  });

  // Close the dropdown if the user clicks anywhere outside of it
  document.addEventListener("click", function (e) {
    if (
      !userMenuButton.contains(e.target) &&
      !userDropdown.contains(e.target)
    ) {
      userDropdown.classList.add("hidden");
    }
  });

  // Prevent clicks inside the dropdown from closing it
  userDropdown.addEventListener("click", function (e) {
    e.stopPropagation();
  });

  // Toggle mobile menu
  const menuToggleButton = document.querySelector(
    "[data-collapse-toggle='navbar-user']"
  );
  const navbarUser = document.getElementById("navbar-user");

  if (menuToggleButton) {
    menuToggleButton.addEventListener("click", function () {
      navbarUser.classList.toggle("hidden");
    });
  }

  document.getElementById('menu-toggle')?.addEventListener('click', function () {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
  });
});