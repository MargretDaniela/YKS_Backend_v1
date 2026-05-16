// //  ── Load Font Awesome if not already loaded ──────────────────────────
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

// });

// ── Load Font Awesome if not already loaded ──────────────────────────
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

    // ── Replace padlock icon with eye toggle on login page ───────────
    var pwdInput = document.querySelector('input[name="password"]');
    if (pwdInput) {
        // Find the existing padlock icon span and replace it
        var inputGroup = pwdInput.closest('.input-group');
        if (inputGroup) {
            var lockSpan = inputGroup.querySelector('.input-group-text');
            if (lockSpan) {
                // Replace padlock with clickable eye icon
                lockSpan.style.cursor  = 'pointer';
                lockSpan.style.userSelect = 'none';
                lockSpan.innerHTML = '<i id="login_eye_icon" class="fas fa-eye" style="font-size:14px;color:#6c757d;"></i>';
                lockSpan.title = 'Show / Hide password';

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

});