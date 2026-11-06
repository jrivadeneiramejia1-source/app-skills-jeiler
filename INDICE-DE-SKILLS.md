# Índice de skills (cuándo usar cada una)

## A. Probar y verificar
| Skill | Cuándo usarla | Origen |
|---|---|---|
| **verificar-app** | Terminé o cambié una app: probar todo, intentar romperla y dar un informe. | Original |
| verification-before-completion | Antes de decir «listo»: exige correr comandos y ver el resultado. | superpowers (MIT) |
| systematic-debugging | Hay un bug: buscar la causa real paso a paso. | superpowers (MIT) |
| test-driven-development | Escribir pruebas y luego el código; arreglar un bug con prueba que lo reproduce. | agent-skills de Addy Osmani (MIT) |
| webapp-testing | Probar una app web local con navegador automático y capturas. | Anthropic (Apache-2.0) |
| playwright-cli | Controlar el navegador por comandos y probar páginas. | Microsoft Playwright (Apache-2.0) |
| browser-testing-with-devtools | Revisar consola, red y rendimiento con las herramientas del navegador. | agent-skills (MIT) |
| code-review-and-quality | Revisar el código en cinco ejes (corrección, claridad, arquitectura, seguridad, rendimiento). | agent-skills (MIT) |
| requesting-code-review / receiving-code-review | Pedir una revisión y responder a los comentarios sin discutir de más. | superpowers (MIT) |
| security-and-hardening | Revisar y reforzar la seguridad de la app. | agent-skills (MIT) |
| shipping-and-launch | Lista de revisión antes de publicar. | agent-skills (MIT) |

## B. Calidad web
| Skill | Cuándo usarla | Origen |
|---|---|---|
| web-quality-audit | Auditoría general (Lighthouse). | web-quality-skills de Addy Osmani (MIT) |
| accessibility | Teclado, contraste, lectores de pantalla. | web-quality-skills (MIT) |
| core-web-vitals | Medir velocidad percibida (LCP, INP, CLS). | web-quality-skills (MIT) |
| performance | La página carga lento. | web-quality-skills (MIT) |
| best-practices | Seguridad y buenas prácticas del navegador. | web-quality-skills (MIT) |
| performance-optimization | Medir primero y optimizar después. | agent-skills (MIT) |

## C. Interfaz
| Skill | Cuándo usarla | Origen |
|---|---|---|
| ui-ux-pro-max | Elegir estilo, colores, tipografías y reglas de UX. | ui-ux-pro-max-skill (MIT) |
| design-system | Colores, tamaños y componentes ordenados como sistema. | ui-ux-pro-max-skill (MIT) |
| frontend-design | Que la interfaz se vea cuidada y no genérica. | Anthropic (Apache-2.0) |
| frontend-ui-engineering | Construir componentes accesibles y bien organizados. | agent-skills (MIT) |
| theme-factory | Aplicar un tema de colores y letras. | Anthropic (Apache-2.0) |
| canvas-design | Pósters y piezas visuales en PNG o PDF (por ejemplo, tarjetas de felicitación). | Anthropic (Apache-2.0) |
| design-taste-frontend | Evitar el aspecto «hecho por IA»; buen gusto en el diseño. | taste-skill (MIT) |
| high-end-visual-design | Look elegante y de alta gama. | taste-skill (MIT) |
| minimalist-ui | Diseño limpio y minimalista. | taste-skill (MIT) |
| redesign-existing-projects | Mejorar el diseño de una app que ya existe. | taste-skill (MIT) |
| vercel-react-best-practices | Código React rápido y ordenado. | Vercel (MIT) |
| vercel-composition-patterns | Componentes React que no se vuelven un enredo. | Vercel (MIT) |

## D. Fluidez
| Skill | Cuándo usarla | Origen |
|---|---|---|
| **fluidez-interfaz** | Que moverse entre páginas y pantallas se sienta suave, sin adornos. | Original |
| vercel-react-view-transitions | Transiciones entre vistas en React. | Vercel (MIT) |

## E. PWA y calidad automática
| Skill | Cuándo usarla | Origen |
|---|---|---|
| **pwa-completa** | Construir una PWA: manifest, service worker, sin internet, datos en el dispositivo, instalación. Trae `revisar_pwa.py` y una guía para publicar en Cloudflare Pages. | Original |
| pwa-review | Auditar una PWA ya hecha (209 puntos, con evidencia). Usarla con la dirección publicada: en modo «solo código» no confirma el manifest ni el service worker (se vio al probarla sobre `asesor-prompts`). | NexFabric (MIT) |
| **ci-calidad-web** | Revisión automática en GitHub Actions: pruebas, claves, dependencias y Lighthouse. Trae una plantilla. | Original |

## F. Antes de construir
| Skill | Cuándo usarla | Origen |
|---|---|---|
| **estudiar-app-referencia** | Estudiar 3 a 5 apps parecidas (licencia, funciones, errores comunes) y escribir una especificación. Trae una tabla de apps abiertas para las apps de Jeiler. | Original |
| **elegir-diseno** | Elegir colores, letras y espacios partiendo de sistemas de diseño ya probados. | Original |

## Plugins oficiales recomendados (se instalan desde el directorio de plugins, no desde este repo)
`playwright`, `typescript-lsp`, `security-guidance`, `code-review` y `pr-review-toolkit`, del directorio oficial de Anthropic (`anthropics/claude-plugins-official`).

## Evaluadas y NO incluidas
- `voidmatcha/e2e-skills` (Apache-2.0): pensada para `@playwright/test` y agentes especiales de Playwright, con scripts propios. Las pruebas de `asesor-prompts` son scripts de Playwright hechos a mano; hoy no encajan.

## Notas
- Las skills de Vercel `vercel-react-best-practices`, `vercel-composition-patterns` y `vercel-react-view-transitions` declaran licencia MIT en su propio `SKILL.md`.
- Se quitó `web-design-guidelines` (Vercel): ni su archivo ni el repo de origen declaran licencia.
- Las licencias de las demás están en `third-party/`.
