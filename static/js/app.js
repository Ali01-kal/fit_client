(function () {
  const root = document.documentElement;
  const BODY = document.body;

  function bySel(sel, ctx) {
    return (ctx || document).querySelector(sel);
  }
  function bySelAll(sel, ctx) {
    return Array.from((ctx || document).querySelectorAll(sel));
  }

  const translations = {
    ru: {
      "nav.home": "Главная",
      "nav.clients": "Клиенты",
      "nav.programs": "Программы",
      "nav.memberships": "Абонементы",
      "nav.reviews": "Отзывы",
      "nav.reports": "Отчёты",
      "nav.account": "Аккаунт",
      "nav.profile": "Профиль",
      "nav.dashboard": "Панель",
      "nav.logout": "Выйти",
      "nav.login": "Войти",
      "nav.register": "Регистрация",
      "nav.contact": "Контакты",
      "footer.quick_links": "Быстрые ссылки",
      "footer.about": "О проекте",
      "footer.system_stats": "Статистика системы",
      "footer.trainers": "Тренеры",
      "footer.template_credit": "Шаблон",
      "footer.template_desc": "Дизайн основан на бесплатном шаблоне Gymnast.",
      "footer.author": "Автор",
    },
    kk: {
      "nav.home": "Басты бет",
      "nav.clients": "Клиенттер",
      "nav.programs": "Бағдарламалар",
      "nav.memberships": "Абонементтер",
      "nav.reviews": "Пікірлер",
      "nav.reports": "Есептер",
      "nav.account": "Аккаунт",
      "nav.profile": "Профиль",
      "nav.dashboard": "Панель",
      "nav.logout": "Шығу",
      "nav.login": "Кіру",
      "nav.register": "Тіркелу",
      "nav.contact": "Байланыс",
      "footer.quick_links": "Жылдам сілтемелер",
      "footer.about": "Жоба туралы",
      "footer.system_stats": "Жүйе статистикасы",
      "footer.trainers": "Жаттықтырушылар",
      "footer.template_credit": "Шаблон ақпараты",
      "footer.template_desc": "Дизайн Gymnast тегін шаблоны негізінде жасалған.",
      "footer.author": "Автор",
    },
  };

  function applyLanguage(lang) {
    const selected = translations[lang] ? lang : "ru";
    root.setAttribute("lang", selected === "kk" ? "kk" : "ru");
    root.setAttribute("data-lang", selected);
    localStorage.setItem("fitclient-lang", selected);
    bySelAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      const nextText = translations[selected][key];
      if (nextText) el.textContent = nextText;
    });
    const langBtn = bySel("[data-lang-toggle]");
    if (langBtn) {
      langBtn.textContent = selected.toUpperCase() === "RU" ? "KZ" : "RU";
      langBtn.setAttribute("title", selected === "ru" ? "Қазақшаға ауыстыру" : "Переключить на русский");
    }
  }

  // 1) Theme toggle + 2) localStorage persistence + 3) initial theme restore
  const savedTheme = localStorage.getItem("fitclient-theme");
  root.setAttribute("data-theme", savedTheme || "light");
  const themeBtn = bySel("[data-theme-toggle]");
  const setThemeBtnLabel = () => {
    if (!themeBtn) return;
    const dark = root.getAttribute("data-theme") === "dark";
    themeBtn.textContent = dark ? "Light" : "Dark";
    themeBtn.setAttribute("title", dark ? "Switch to light theme" : "Switch to dark theme");
  };
  setThemeBtnLabel();
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("fitclient-theme", next);
      setThemeBtnLabel();
    });
  }

  // 4) Language toggle (UI labels)
  const savedLang = localStorage.getItem("fitclient-lang") || "ru";
  applyLanguage(savedLang);
  const langBtn = bySel("[data-lang-toggle]");
  if (langBtn) {
    langBtn.addEventListener("click", () => {
      const current = root.getAttribute("data-lang") || "ru";
      applyLanguage(current === "ru" ? "kk" : "ru");
    });
  }

  // 5) Client-side required validation hints
  bySelAll("form[data-validate]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      let firstInvalid = null;
      bySelAll("[required]", form).forEach((el) => {
        if (!el.value.trim()) {
          el.setAttribute("aria-invalid", "true");
          firstInvalid = firstInvalid || el;
        } else {
          el.removeAttribute("aria-invalid");
        }
      });
      if (firstInvalid) {
        e.preventDefault();
        firstInvalid.focus();
      }
    });
  });

  // 6) Email format lightweight validation
  bySelAll("input[type='email']").forEach((input) => {
    input.addEventListener("blur", () => {
      if (!input.value) return;
      const ok = /.+@.+\..+/.test(input.value);
      input.setCustomValidity(ok ? "" : "Введите корректный email");
    });
  });

  // 7) Live card filtering (UI only)
  bySelAll("[data-live-filter]").forEach((form) => {
    const target = bySel("#live-filter-target");
    const search = bySel("input[type='search']", form);
    if (!target || !search) return;
    search.addEventListener("input", () => {
      const q = search.value.toLowerCase().trim();
      bySelAll(".card", target).forEach((card) => {
        card.style.display = card.textContent.toLowerCase().includes(q) ? "" : "none";
      });
    });
  });

  // 8) Flash autoclose
  bySelAll(".flash").forEach((msg) => {
    setTimeout(() => {
      msg.style.opacity = "0";
      setTimeout(() => msg.remove(), 250);
    }, 3500);
  });

  // 9) Keyboard shortcut "/" to focus first search field
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) {
      const search = bySel("input[type='search']");
      if (search) {
        e.preventDefault();
        search.focus();
      }
    }
  });

  // 10) Smooth reveal class on load
  bySelAll(".reveal").forEach((el, index) => {
    el.style.animationDelay = `${index * 80}ms`;
  });

  // 11) Table row hover state
  bySelAll(".data-table tbody tr").forEach((tr) => {
    tr.addEventListener("mouseenter", () => (tr.style.background = "rgba(17,100,102,.05)"));
    tr.addEventListener("mouseleave", () => (tr.style.background = ""));
  });

  // 12) Auto-resize textareas
  bySelAll("textarea").forEach((ta) => {
    const fit = () => {
      ta.style.height = "auto";
      ta.style.height = ta.scrollHeight + "px";
    };
    ta.addEventListener("input", fit);
    fit();
  });

  // 13) Numeric guard for phone-ish inputs
  bySelAll("input[name='phone']").forEach((input) => {
    input.addEventListener("input", () => {
      input.value = input.value.replace(/[^\d+\-()\s]/g, "");
    });
  });

  // 14) Pending button state
  bySelAll("form button[type='submit']").forEach((btn) => {
    btn.form?.addEventListener("submit", () => {
      btn.dataset.originalText = btn.textContent;
      btn.textContent = "Сохранение...";
      btn.disabled = true;
    });
  });

  // 15) Dummy modal support (hook for future features)
  const modalBackdrop = document.createElement("div");
  modalBackdrop.className = "modal-backdrop";
  modalBackdrop.innerHTML = '<div class="modal" role="dialog" aria-modal="true"><h2>Подсказка</h2><p>Нажмите "/" для быстрого поиска по странице.</p><button class="btn btn--accent" type="button">Ок</button></div>';
  document.body.appendChild(modalBackdrop);
  const hideModal = () => modalBackdrop.classList.remove("is-open");
  modalBackdrop.addEventListener("click", (e) => {
    if (e.target === modalBackdrop) hideModal();
  });
  bySel("button", modalBackdrop).addEventListener("click", hideModal);
  if (!localStorage.getItem("fitclient-tip-shown")) {
    setTimeout(() => {
      modalBackdrop.classList.add("is-open");
      localStorage.setItem("fitclient-tip-shown", "1");
    }, 900);
  }

  // 16) Escape closes modal
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") hideModal();
  });

  // 17) Force custom styled selects for auth forms (Windows native select popup ignores CSS)
  if (window.jQuery && typeof window.jQuery.fn.niceSelect === "function") {
    window.jQuery(".zc-auth-form select").each(function () {
      const $select = window.jQuery(this);
      if ($select.next(".nice-select").length) return;
      $select.niceSelect();
    });
  }
})();
