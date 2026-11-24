# Lista corta de seguridad · Short security checklist (R06)

> Lista mínima para revisar antes de producción, inspirada en OWASP ASVS 5.0 nivel 1. **No reemplaza la lista completa** de ASVS: es el punto de partida para alguien que trabaja solo. Lo no cubierto se anota en `docs/ESTADO.md`.
> *Minimal pre-production checklist inspired by OWASP ASVS 5.0 level 1. It does not replace the full ASVS list.*

- [ ] **Login:** viene del framework (en Django, `django.contrib.auth`); contraseñas con su hasheo por defecto; límite de intentos fallidos. · *Framework login, default hashing, failed-attempt limit.*
- [ ] **Sesión:** cookies `Secure`, `HttpOnly` y `SameSite`; la sesión se cierra al salir y vence por inactividad. · *Secure cookies; logout and idle timeout.*
- [ ] **Permisos:** cada vista revisa el permiso en el servidor; cada rol tiene una prueba de lo que **no** puede hacer. · *Server-side checks; negative tests per role.*
- [ ] **Datos de otro:** nadie ve ni cambia un registro ajeno cambiando un número en la URL; un id ajeno da el mismo 404 que uno inexistente. Prueba de ejemplo (Django): [`ejemplos/test_aislamiento_django.py`](https://github.com/tarazonawin-stack/auroratk/blob/v3.0.0/ejemplos/test_aislamiento_django.py). · *No access to others' records by editing an ID; same 404 as a missing one.*
- [ ] **Entradas:** todo formulario se valida en el servidor; consultas solo con el ORM o parámetros, nunca armando SQL con texto. · *Server-side validation; ORM or parameters only.*
- [ ] **Salida:** las plantillas escapan el HTML (sin `|safe` ni `mark_safe` con datos de usuarios). · *Escaped output.*
- [ ] **CSRF:** activo en todos los formularios. · *CSRF on every form.*
- [ ] **Archivos subidos:** tipo y tamaño limitados; se guardan fuera del código y no se ejecutan. · *Type and size limits; stored outside code.*
- [ ] **Configuración:** `DEBUG = False`, `ALLOWED_HOSTS` definido, HTTPS con HSTS, y `check --deploy` sin avisos. · *Production settings.*
- [ ] **Errores:** el usuario ve un mensaje claro, nunca la traza técnica. · *No stack traces to users.*
- [ ] **Registros:** inicios de sesión fallidos y cambios de permisos quedan registrados con el ID interno (R14). · *Security events logged with internal IDs.*
- [ ] **Secretos:** ninguno en el repo ni en el navegador; `.env.example` al día (R05). · *No secrets in repo or browser.*
