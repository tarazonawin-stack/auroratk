# Antes de datos reales · Before real data

> Copia a `docs/datos-reales.md`. Ningún dato real de una persona entra al sistema hasta que todas las casillas estén marcadas, con su evidencia fechada en `docs/evidencia/`, o con una excepción con fecha en `docs/excepciones.md`. Lo revisa una persona, no la IA que construyó (R12, riesgo 3).
> *Copy to `docs/datos-reales.md`. No real personal data until every box is checked with dated evidence, or a dated exception. A person reviews it, not the AI that built it.*

## Seguridad · Security (R05, R06)
- [ ] Escáner de secretos sin hallazgos en todo el historial · *Secret scan clean over the whole history*
- [ ] `asvs-corto.md` completa; ASVS 5.0 nivel 1 (Estándar) o 2 (Estricto); lo no cubierto, anotado · *Short checklist done; ASVS level 1/2; gaps written down*
- [ ] Prueba de aislamiento en verde: toda URL exige login y un id ajeno da el mismo 404 que uno inexistente (ejemplo: `ejemplos/test_aislamiento_django.py`) · *Isolation test green*
- [ ] Pruebas de lo que cada rol **no** puede hacer · *Negative tests per role*

## Datos · Data (R08)
- [ ] Respaldo automático y **una restauración probada**, en un entorno aislado que se borra al terminar · *Automatic backup and one tested restore*
- [ ] Migraciones reversibles; las que no, en dos pasos y con plan escrito · *Reversible migrations, or two-step with a plan*

## Privacidad · Privacy (R09, perfil de país · country profile)
- [ ] Inventario de datos personales: qué, para qué, plazo y cómo se borra · *Personal data inventory: what, why, how long, how deleted*
- [ ] Base legal o consentimiento registrado; aviso de privacidad visible (ES/EN) · *Legal basis or recorded consent; visible notice*
- [ ] Funciones para ver, corregir, exportar y borrar (o anonimizar) los datos de una persona · *View, fix, export, delete or anonymize*
- [ ] Procedimiento de filtración escrito, con plazos de ley (Perú: 48 h a la ANPD) · *Written breach procedure with legal deadlines*
- [ ] Documento de seguridad, roles (titular y encargado) e inscripción del banco de datos, si el perfil de país lo pide · *Security document, roles and database registration if required*
- [ ] Perfil de país validado por un abogado, con fecha · *Country profile validated by a lawyer, dated*

## Operar · Operate (R14, R16)
- [ ] Alerta de error grave probada: le llegó a una persona · *Serious-error alert tested: it reached a person*
- [ ] Despliegue desde el CI con aprobación, comprobación posterior y **vuelta atrás probada** · *CI deployment with approval, post-deploy check and tested rollback*
- [ ] Quién responde ante un incidente y cómo se le avisa · *Who answers an incident and how they are reached*
