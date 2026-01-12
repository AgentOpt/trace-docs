import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

/**
 * Shared layout configurations
 *
 * you can customise layouts individually from:
 * Home Layout: app/(home)/layout.tsx
 * Docs Layout: app/docs/layout.tsx
 */
export function baseOptions(): BaseLayoutProps {
  return {
    nav: {
      title: (
        <>
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            aria-label="Trace Logo"
            fill="none"
          >
            <path
              d="M3 12 L9 6 L15 12 L21 6"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M3 18 L9 12 L15 18 L21 12"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              opacity="0.5"
            />
          </svg>
          <span className="font-bold">Trace2</span>
        </>
      ),
    },
    // see https://fumadocs.dev/docs/ui/navigation/links
    links: [
      {
        text: 'Documentation',
        url: '/docs',
        active: 'nested-url',
      },
      {
        text: 'GitHub',
        url: 'https://github.com/AgentOpt/OpenTrace',
        external: true,
      },
      {
        text: 'Paper',
        url: 'https://arxiv.org/abs/2406.16218',
        external: true,
      },
    ],
  };
}
