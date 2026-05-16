
// // ── Load Font Awesome if not already loaded ──────────────────────────
// (function() {
//   var existing = document.querySelector('link[href*="font-awesome"]');
//   if (!existing) {
//     var link = document.createElement('link');
//     link.rel  = 'stylesheet';
//     link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
//     document.head.appendChild(link);
//   }
// })();

// // ── DOM Ready ─────────────────────────────────────────────────────────
// document.addEventListener("DOMContentLoaded", function () {

//     // ── Role badge under username in sidebar ──────────────────────────
//     const userInfo = document.querySelector(".user-panel .info a");
//     if (userInfo) {
//         const roleEl = document.createElement("span");
//         roleEl.style.cssText = (
//             "display:block;font-size:10px;font-weight:700;" +
//             "text-transform:uppercase;letter-spacing:1px;" +
//             "color:rgba(255,255,255,0.4);margin-top:2px;"
//         );
//         const bodyClass = document.body.className;
//         if (bodyClass.includes("super"))       roleEl.textContent = "Super Admin";
//         else if (bodyClass.includes("admin"))  roleEl.textContent = "Admin";
//         else if (bodyClass.includes("mentor")) roleEl.textContent = "Mentor";
//         else                                   roleEl.textContent = "Student";
//         userInfo.parentNode.appendChild(roleEl);
//     }

//     // ── Animated sidebar toggle for mobile ────────────────────────────
//     const toggleBtn = document.querySelector('[data-widget="pushmenu"]');
//     if (toggleBtn) {
//         toggleBtn.addEventListener("click", function () {
//             document.body.classList.toggle("sidebar-open");
//         });
//     }

//     // ── Replace padlock icon with eye toggle on login page ────────────
//     var pwdInput = document.querySelector('input[name="password"]');
//     if (pwdInput) {
//         var inputGroup = pwdInput.closest('.input-group');
//         if (inputGroup) {
//             var lockSpan = inputGroup.querySelector('.input-group-text');
//             if (lockSpan) {
//                 lockSpan.style.cursor     = 'pointer';
//                 lockSpan.style.userSelect = 'none';
//                 lockSpan.innerHTML        = '<i id="login_eye_icon" class="fas fa-eye" style="font-size:14px;color:#6c757d;"></i>';
//                 lockSpan.title            = 'Show / Hide password';

//                 lockSpan.addEventListener('click', function () {
//                     var icon = document.getElementById('login_eye_icon');
//                     if (pwdInput.type === 'password') {
//                         pwdInput.type  = 'text';
//                         icon.className = 'fas fa-eye-slash';
//                     } else {
//                         pwdInput.type  = 'password';
//                         icon.className = 'fas fa-eye';
//                     }
//                 });
//             }
//         }
//     }

//     // ── Pages Dashboard collapsible dropdown in sidebar ───────────────
//     const allLinks = document.querySelectorAll(".nav-sidebar .nav-link");
//     let pagesDashboardLink = null;

//     allLinks.forEach(function (link) {
//         if (link.textContent.trim().includes("Pages Dashboard")) {
//             pagesDashboardLink = link;
//         }
//     });

//     if (pagesDashboardLink) {
//         const parentLi = pagesDashboardLink.closest("li.nav-item");

//         if (parentLi) {
//             const dropdownItems = [
//                 { icon: "fas fa-image",              label: "Banners",           url: "/admin/pages/homebanner/" },
//                 { icon: "fas fa-star",               label: "Featured Courses",  url: "/admin/pages/homefeaturedcourse/" },
//                 { icon: "fas fa-th-large",           label: "Home Sections",     url: "/admin/pages/homesection/" },
//                 { icon: "fas fa-graduation-cap",     label: "All Courses",       url: "/admin/courses/course/" },
//                 { icon: "fas fa-tags",               label: "Categories",        url: "/admin/pages/coursecategory/" },
//                 { icon: "fas fa-user-graduate",      label: "Enrollments",       url: "/admin/courses/enrollment/" },
//                 { icon: "fas fa-users",              label: "All Users",         url: "/admin/accounts/user/" },
//                 { icon: "fas fa-calendar-check",     label: "Attendance",        url: "/admin/attendance/attendance/" },
//                 { icon: "fas fa-chalkboard-teacher", label: "Sessions",          url: "/admin/mentorship/mentorshipsession/" },
//                 { icon: "fas fa-file-alt",           label: "Info Pages",        url: "/admin/pages/infopage/" },
//                 { icon: "fas fa-cog",                label: "Site Settings",     url: "/admin/pages/sitesettings/" },
//             ];

//             // Build sub-menu
//             const subUl         = document.createElement("ul");
//             subUl.className     = "nav nav-treeview";
//             subUl.style.display = "none";

//             dropdownItems.forEach(function (item) {
//                 const li     = document.createElement("li");
//                 li.className = "nav-item";
//                 li.innerHTML = `
//                     <a href="${item.url}" class="nav-link" style="padding-left:2rem;">
//                         <i class="nav-icon ${item.icon}" style="font-size:12px;"></i>
//                         <p style="font-size:12px;">${item.label}</p>
//                     </a>`;
//                 subUl.appendChild(li);
//             });

//             // Add arrow to Pages Dashboard link
//             parentLi.classList.add("has-treeview");
//             const arrow            = document.createElement("i");
//             arrow.className        = "right fas fa-angle-left";
//             arrow.style.transition = "transform 0.2s";
//             pagesDashboardLink.appendChild(arrow);
//             parentLi.appendChild(subUl);

//             // Toggle on click
//             let open = false;
//             pagesDashboardLink.addEventListener("click", function (e) {
//                 e.preventDefault();
//                 open                  = !open;
//                 subUl.style.display   = open ? "block" : "none";
//                 arrow.style.transform = open ? "rotate(-90deg)" : "rotate(0deg)";
//             });
//         }
//     }

// });
(function() {
  var existing = document.querySelector('link[href*="font-awesome"]');
  if (!existing) {
    var link = document.createElement('link');
    link.rel  = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
    document.head.appendChild(link);
  }
})();

// ── DOM Ready ─────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", function () {

    // ── Replace avatar with logo in sidebar user-panel ────────────────
    var userPanel = document.querySelector(".user-panel");
    if (userPanel) {
        // Hide any existing image container (the letter-avatar circle)
        var existingImg = userPanel.querySelector(".image");
        if (existingImg) {
            existingImg.style.display = "none";
        }

        // Also hide any <img> tags directly inside .user-panel
        var directImgs = userPanel.querySelectorAll("img");
        directImgs.forEach(function(img) {
            img.style.display = "none";
        });

        // Build logo wrapper and inject before .info
        var logoWrap = document.createElement("div");
        logoWrap.className = "yk-logo-wrap";

        var logoImg = document.createElement("img");
        // ── LOGO PATH — update this to your actual static logo path ──
        logoImg.src = "/static/img/logo.png";
        logoImg.alt = "Youth Key Series";
        logoImg.style.cssText = (
            "width:40px;height:40px;object-fit:contain;" +
            "border-radius:8px;display:block;"
        );

        // Fallback: if logo fails to load, show a styled text badge
        logoImg.onerror = function() {
            logoWrap.removeChild(logoImg);
            var fallback = document.createElement("div");
            fallback.style.cssText = (
                "width:40px;height:40px;border-radius:8px;" +
                "background:linear-gradient(135deg,#AC7D0C,#D4A017);" +
                "display:flex;align-items:center;justify-content:center;" +
                "font-size:14px;font-weight:800;color:#fff;letter-spacing:0.5px;"
            );
            fallback.textContent = "YK";
            logoWrap.appendChild(fallback);
        };

        logoWrap.appendChild(logoImg);

        // Insert logo before the .info div
        var infoDiv = userPanel.querySelector(".info");
        if (infoDiv) {
            userPanel.insertBefore(logoWrap, infoDiv);
        } else {
            userPanel.prepend(logoWrap);
        }

        // Make user-panel flex so logo + info sit side by side
        userPanel.style.cssText += (
            "display:flex !important;" +
            "align-items:center !important;" +
            "flex-direction:row !important;"
        );
    }

    // ── Role badge under username in sidebar ──────────────────────────
    const userInfo = document.querySelector(".user-panel .info a");
    if (userInfo) {
        const roleEl = document.createElement("span");
        roleEl.style.cssText = (
            "display:block;font-size:10px;font-weight:700;" +
            "text-transform:uppercase;letter-spacing:1px;" +
            "color:rgba(255,255,255,0.4);margin-top:2px;"
        );
        const bodyClass = document.body.className;
        if (bodyClass.includes("super"))       roleEl.textContent = "Super Admin";
        else if (bodyClass.includes("admin"))  roleEl.textContent = "Admin";
        else if (bodyClass.includes("mentor")) roleEl.textContent = "Mentor";
        else                                   roleEl.textContent = "Student";
        userInfo.parentNode.appendChild(roleEl);
    }

    // ── Animated sidebar toggle for mobile ────────────────────────────
    const toggleBtn = document.querySelector('[data-widget="pushmenu"]');
    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            document.body.classList.toggle("sidebar-open");
        });
    }

    // ── Replace padlock icon with eye toggle on login page ────────────
    var pwdInput = document.querySelector('input[name="password"]');
    if (pwdInput) {
        var inputGroup = pwdInput.closest('.input-group');
        if (inputGroup) {
            var lockSpan = inputGroup.querySelector('.input-group-text');
            if (lockSpan) {
                lockSpan.style.cursor     = 'pointer';
                lockSpan.style.userSelect = 'none';
                lockSpan.innerHTML        = '<i id="login_eye_icon" class="fas fa-eye" style="font-size:14px;color:#6c757d;"></i>';
                lockSpan.title            = 'Show / Hide password';

                lockSpan.addEventListener('click', function () {
                    var icon = document.getElementById('login_eye_icon');
                    if (pwdInput.type === 'password') {
                        pwdInput.type  = 'text';
                        icon.className = 'fas fa-eye-slash';
                    } else {
                        pwdInput.type  = 'password';
                        icon.className = 'fas fa-eye';
                    }
                });
            }
        }
    }

    // ── Pages Dashboard collapsible dropdown in sidebar ───────────────
    const allLinks = document.querySelectorAll(".nav-sidebar .nav-link");
    let pagesDashboardLink = null;

    allLinks.forEach(function (link) {
        if (link.textContent.trim().includes("Pages Dashboard")) {
            pagesDashboardLink = link;
        }
    });

    if (pagesDashboardLink) {
        const parentLi = pagesDashboardLink.closest("li.nav-item");

        if (parentLi) {
            const dropdownItems = [
                { icon: "fas fa-image",              label: "Banners",           url: "/admin/pages/homebanner/" },
                { icon: "fas fa-star",               label: "Featured Courses",  url: "/admin/pages/homefeaturedcourse/" },
                { icon: "fas fa-th-large",           label: "Home Sections",     url: "/admin/pages/homesection/" },
                { icon: "fas fa-graduation-cap",     label: "All Courses",       url: "/admin/courses/course/" },
                { icon: "fas fa-tags",               label: "Categories",        url: "/admin/pages/coursecategory/" },
                { icon: "fas fa-user-graduate",      label: "Enrollments",       url: "/admin/courses/enrollment/" },
                { icon: "fas fa-users",              label: "All Users",         url: "/admin/accounts/user/" },
                { icon: "fas fa-calendar-check",     label: "Attendance",        url: "/admin/attendance/attendance/" },
                { icon: "fas fa-chalkboard-teacher", label: "Sessions",          url: "/admin/mentorship/mentorshipsession/" },
                { icon: "fas fa-file-alt",           label: "Info Pages",        url: "/admin/pages/infopage/" },
                { icon: "fas fa-cog",                label: "Site Settings",     url: "/admin/pages/sitesettings/" },
            ];

            // Build sub-menu
            const subUl         = document.createElement("ul");
            subUl.className     = "nav nav-treeview";
            subUl.style.display = "none";

            dropdownItems.forEach(function (item) {
                const li     = document.createElement("li");
                li.className = "nav-item";
                li.innerHTML = `
                    <a href="${item.url}" class="nav-link" style="padding-left:2rem;">
                        <i class="nav-icon ${item.icon}" style="font-size:12px;"></i>
                        <p style="font-size:12px;">${item.label}</p>
                    </a>`;
                subUl.appendChild(li);
            });

            // Add arrow to Pages Dashboard link
            parentLi.classList.add("has-treeview");
            const arrow            = document.createElement("i");
            arrow.className        = "right fas fa-angle-left";
            arrow.style.transition = "transform 0.2s";
            pagesDashboardLink.appendChild(arrow);
            parentLi.appendChild(subUl);

            // Toggle on click
            let open = false;
            pagesDashboardLink.addEventListener("click", function (e) {
                e.preventDefault();
                open                  = !open;
                subUl.style.display   = open ? "block" : "none";
                arrow.style.transform = open ? "rotate(-90deg)" : "rotate(0deg)";
            });
        }
    }

});