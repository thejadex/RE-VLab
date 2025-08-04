// Requirements Lab JavaScript functionality

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  initializeTooltips()

  // Initialize modals
  initializeModals()

  // Initialize notifications
  initializeNotifications()

  // Initialize form enhancements
  initializeFormEnhancements()

  // Initialize search functionality
  initializeSearch()
})

function initializeTooltips() {
  // Add tooltip functionality for elements with data-tooltip attribute
  const tooltipElements = document.querySelectorAll("[data-tooltip]")

  tooltipElements.forEach((element) => {
    element.addEventListener("mouseenter", showTooltip)
    element.addEventListener("mouseleave", hideTooltip)
  })
}

function showTooltip(event) {
  const tooltip = document.createElement("div")
  tooltip.className = "absolute bg-gray-800 text-white text-sm px-2 py-1 rounded shadow-lg z-50"
  tooltip.textContent = event.target.getAttribute("data-tooltip")
  tooltip.id = "tooltip"

  document.body.appendChild(tooltip)

  const rect = event.target.getBoundingClientRect()
  tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + "px"
  tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + "px"
}

function hideTooltip() {
  const tooltip = document.getElementById("tooltip")
  if (tooltip) {
    tooltip.remove()
  }
}

function initializeModals() {
  // Modal functionality
  window.openModal = (modalId) => {
    const modal = document.getElementById(modalId)
    if (modal) {
      modal.classList.remove("hidden")
      modal.querySelector(".modal-content")?.classList.add("modal-enter")
    }
  }

  window.closeModal = (modalId) => {
    const modal = document.getElementById(modalId)
    if (modal) {
      modal.classList.add("hidden")
    }
  }

  // Close modal when clicking outside
  document.addEventListener("click", (event) => {
    if (event.target.classList.contains("modal-backdrop")) {
      event.target.classList.add("hidden")
    }
  })

  // Close modal with Escape key
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      const openModals = document.querySelectorAll(".modal:not(.hidden)")
      openModals.forEach((modal) => modal.classList.add("hidden"))
    }
  })
}

function initializeNotifications() {
  // Auto-hide success messages after 5 seconds
  const successMessages = document.querySelectorAll(".alert-success")
  successMessages.forEach((message) => {
    setTimeout(() => {
      message.style.opacity = "0"
      setTimeout(() => message.remove(), 300)
    }, 5000)
  })

  // Mark notifications as read when clicked
  const notificationItems = document.querySelectorAll(".notification-item")
  notificationItems.forEach((item) => {
    item.addEventListener("click", function () {
      this.classList.remove("unread")
      this.classList.add("read")
    })
  })
}

function initializeFormEnhancements() {
  // Auto-resize textareas
  const textareas = document.querySelectorAll("textarea")
  textareas.forEach((textarea) => {
    textarea.addEventListener("input", function () {
      this.style.height = "auto"
      this.style.height = this.scrollHeight + "px"
    })
  })

  // Form validation enhancements
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      const requiredFields = form.querySelectorAll("[required]")
      let isValid = true

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          field.classList.add("border-red-500")
          isValid = false
        } else {
          field.classList.remove("border-red-500")
        }
      })

      if (!isValid) {
        event.preventDefault()
        showNotification("Please fill in all required fields", "error")
      }
    })
  })
}

// Search functionality
function initializeSearch() {
  const searchInputs = document.querySelectorAll("[data-search]")

  searchInputs.forEach((input) => {
    input.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase()
      const targetSelector = this.getAttribute("data-search")
      const targets = document.querySelectorAll(targetSelector)

      targets.forEach((target) => {
        const text = target.textContent.toLowerCase()
        if (text.includes(searchTerm)) {
          target.style.display = ""
        } else {
          target.style.display = "none"
        }
      })
    })
  })
}

// Utility functions
function showNotification(message, type = "info") {
  const notification = document.createElement("div")
  notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
    type === "error"
      ? "bg-red-500 text-white"
      : type === "success"
        ? "bg-green-500 text-white"
        : type === "warning"
          ? "bg-yellow-500 text-white"
          : "bg-blue-500 text-white"
  }`
  notification.textContent = message

  document.body.appendChild(notification)

  // Auto-remove after 3 seconds
  setTimeout(() => {
    notification.style.opacity = "0"
    setTimeout(() => notification.remove(), 300)
  }, 3000)
}

function confirmAction(message, callback) {
  if (confirm(message)) {
    callback()
  }
}

// Progress bar animation
function animateProgressBar(element, targetWidth) {
  let currentWidth = 0
  const increment = targetWidth / 50

  const animation = setInterval(() => {
    currentWidth += increment
    element.style.width = currentWidth + "%"

    if (currentWidth >= targetWidth) {
      clearInterval(animation)
      element.style.width = targetWidth + "%"
    }
  }, 20)
}

// Export functions for global use
window.RequirementsLab = {
  showNotification,
  confirmAction,
  animateProgressBar,
  openModal,
  closeModal,
}
