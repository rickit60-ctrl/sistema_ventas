// Auto-cerrar flash messages después de 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(-20px)';
            setTimeout(function() {
                flash.remove();
            }, 300);
        }, 5000);
    });
    
    // Animaciones de entrada para elementos
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.stat-card, .dashboard-card, .diezmo-card');
        
        elements.forEach(function(element, index) {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 50) {
                setTimeout(function() {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, index * 100);
            }
        });
    };
    
    // Preparar elementos para animación
    const elements = document.querySelectorAll('.stat-card, .dashboard-card, .diezmo-card');
    elements.forEach(function(element) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.5s ease';
    });
    
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);
});

// Formatear números como moneda
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-DO', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Confirmar acciones peligrosas
function confirmAction(message) {
    return confirm(message || '¿Estás seguro de realizar esta acción?');
}

// Validación de formularios en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const numberInputs = document.querySelectorAll('input[type="number"]');
    
    numberInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (parseFloat(this.value) < 0) {
                this.value = 0;
            }
        });
    });
});

// ========================================
// MENÚ MÓVIL Y NAVEGACIÓN RESPONSIVE
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.sap-nav');
    const body = document.body;
    
    if (menuToggle && nav) {
        // Toggle menú móvil
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            nav.classList.toggle('show');
            body.classList.toggle('nav-open');
        });
        
        // Cerrar menú al hacer click fuera (en el overlay)
        document.addEventListener('click', function(e) {
            if (nav.classList.contains('show')) {
                if (!nav.contains(e.target) && !menuToggle.contains(e.target)) {
                    nav.classList.remove('show');
                    body.classList.remove('nav-open');
                }
            }
        });
        
        // Cerrar menú al hacer click en un enlace (solo en móvil)
        const navLinks = nav.querySelectorAll('.nav-item');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    setTimeout(function() {
                        nav.classList.remove('show');
                        body.classList.remove('nav-open');
                    }, 200);
                }
            });
        });
        
        // Cerrar menú al cambiar orientación
        window.addEventListener('orientationchange', function() {
            nav.classList.remove('show');
            body.classList.remove('nav-open');
        });
        
        // Cerrar menú al hacer resize a desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                nav.classList.remove('show');
                body.classList.remove('nav-open');
            }
        });
    }
});

// ========================================
// SCROLL SUAVE EN TABLAS
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    const tableContainers = document.querySelectorAll('.table-container');
    
    tableContainers.forEach(function(container) {
        let isScrolling;
        
        container.addEventListener('scroll', function() {
            // Ocultar el hint de scroll cuando el usuario empiece a scrollear
            const hint = container.querySelector('::after');
            if (container.scrollLeft > 10) {
                container.style.setProperty('--scroll-hint-opacity', '0');
            }
            
            // Mostrar de nuevo el hint cuando deje de scrollear
            clearTimeout(isScrolling);
            isScrolling = setTimeout(function() {
                if (container.scrollLeft < container.scrollWidth - container.clientWidth - 10) {
                    container.style.setProperty('--scroll-hint-opacity', '0.7');
                }
            }, 1000);
        });
    });
});

// ========================================
// MEJORAS PARA TOUCH
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Prevenir comportamiento de long-press en elementos interactivos
    const interactiveElements = document.querySelectorAll('.btn, .nav-item, a, button');
    
    interactiveElements.forEach(function(element) {
        element.addEventListener('touchstart', function() {
            this.style.webkitTouchCallout = 'none';
        });
    });
    
    // Mejorar feedback visual en touch
    const buttons = document.querySelectorAll('.btn, button');
    buttons.forEach(function(button) {
        let touchTimeout;
        
        button.addEventListener('touchstart', function() {
            touchTimeout = setTimeout(function() {
                // Long press detected
            }, 500);
        });
        
        button.addEventListener('touchend', function() {
            clearTimeout(touchTimeout);
        });
        
        button.addEventListener('touchcancel', function() {
            clearTimeout(touchTimeout);
        });
    });
});

// ========================================
// DETECTAR SCROLL EN TABLAS MÓVILES
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    if (window.innerWidth <= 768) {
        const tables = document.querySelectorAll('.table-container');
        
        tables.forEach(function(table) {
            // Agregar indicador de scroll si la tabla es más ancha que el contenedor
            if (table.scrollWidth > table.clientWidth) {
                table.classList.add('has-scroll');
            }
        });
    }
});

// ========================================
// PREVENIR ZOOM ACCIDENTAL EN iOS
// ========================================

document.addEventListener('touchstart', function(event) {
    if (event.touches.length > 1) {
        event.preventDefault();
    }
}, { passive: false });

let lastTouchEnd = 0;
document.addEventListener('touchend', function(event) {
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {
        event.preventDefault();
    }
    lastTouchEnd = now;
}, false);

// ========================================
// ORIENTACIÓN Y RESPONSIVE HELPERS
// ========================================

function isMobile() {
    return window.innerWidth <= 768;
}

function isTablet() {
    return window.innerWidth > 768 && window.innerWidth <= 1024;
}

function isDesktop() {
    return window.innerWidth > 1024;
}

// Actualizar viewport height para mobile browsers
function updateVH() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

updateVH();
window.addEventListener('resize', updateVH);
window.addEventListener('orientationchange', function() {
    setTimeout(updateVH, 100);
});

// ========================================
// SWIPE GESTURE PARA CERRAR MENÚ
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('.sap-nav');
    const body = document.body;
    
    if (nav && isMobile()) {
        let touchStartX = 0;
        let touchEndX = 0;
        
        nav.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        nav.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
        
        function handleSwipe() {
            if (touchStartX - touchEndX > 50) {
                // Swipe left - cerrar menú
                nav.classList.remove('show');
                body.classList.remove('nav-open');
            }
        }
    }
});

// ========================================
// SCROLL TO TOP EN MOBILE
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    if (isMobile()) {
        // Scroll to top cuando se navega a una nueva página
        window.scrollTo(0, 0);
        
        // Agregar botón flotante de scroll to top
        const scrollBtn = document.createElement('button');
        scrollBtn.innerHTML = '↑';
        scrollBtn.className = 'scroll-to-top';
        scrollBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--sap-primary);
            color: white;
            border: none;
            font-size: 24px;
            cursor: pointer;
            display: none;
            z-index: 999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(scrollBtn);
        
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollBtn.style.display = 'block';
            } else {
                scrollBtn.style.display = 'none';
            }
        });
        
        scrollBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});

// ========================================
// HELPERS PARA FORMULARIOS MÓVILES
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    if (isMobile()) {
        // Auto-scroll al input cuando recibe focus (prevenir que quede detrás del teclado)
        const inputs = document.querySelectorAll('input, textarea, select');
        
        inputs.forEach(function(input) {
            input.addEventListener('focus', function() {
                setTimeout(function() {
                    input.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 300);
            });
        });
    }
});

