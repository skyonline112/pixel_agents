import type { AgentEvent, HookProvider } from '../../../../../core/src/provider.js';

export function formatToolStatus(toolName: string, _input?: unknown): string {
  switch (toolName) {
    case 'Classifier':
      return '민원 분석 중...';
    case 'Searcher':
      return '법령/자료 검색 중...';
    case 'Drafter':
      return '답변 초안 작성 중...';
    case 'Reviewer':
      return '초안 최종 검수 중...';
    default:
      return `${toolName} 실행 중...`;
  }
}

function normalizeHookEvent(
  raw: Record<string, unknown>,
): { sessionId: string; event: AgentEvent } | null {
  const eventName = raw.hook_event_name;
  const sessionId = raw.session_id;
  if (typeof eventName !== 'string' || typeof sessionId !== 'string') return null;

  switch (eventName) {
    case 'SessionStart':
      return {
        sessionId,
        event: {
          kind: 'sessionStart',
          cwd: typeof raw.cwd === 'string' ? raw.cwd : undefined,
        },
      };

    case 'SessionEnd':
      return {
        sessionId,
        event: {
          kind: 'sessionEnd',
          reason: typeof raw.reason === 'string' ? raw.reason : undefined,
        },
      };

    case 'PreToolUse': {
      const toolName = typeof raw.tool_name === 'string' ? raw.tool_name : '';
      const toolInput =
        typeof raw.tool_input === 'object' && raw.tool_input !== null
          ? (raw.tool_input as Record<string, unknown>)
          : {};
      return {
        sessionId,
        event: {
          kind: 'toolStart',
          toolId: typeof raw.tool_id === 'string' ? raw.tool_id : `hook-${Date.now()}`,
          toolName,
          input: toolInput,
          runInBackground: toolInput.run_in_background === true,
        },
      };
    }

    case 'PostToolUse':
    case 'PostToolUseFailure':
      return {
        sessionId,
        event: {
          kind: 'toolEnd',
          toolId: typeof raw.tool_id === 'string' ? raw.tool_id : 'current',
        },
      };

    case 'SubagentStart': {
      const agentType = typeof raw.agent_type === 'string' ? raw.agent_type : 'unknown';
      return {
        sessionId,
        event: {
          kind: 'subagentStart',
          parentToolId: 'current',
          toolId: typeof raw.tool_id === 'string' ? raw.tool_id : `hook-sub-${agentType}-${Date.now()}`,
          toolName: agentType,
          input: raw,
          runInBackground: raw.run_in_background === true,
        },
      };
    }

    case 'SubagentStop':
      return {
        sessionId,
        event: {
          kind: 'subagentEnd',
          parentToolId: 'current',
          toolId: typeof raw.tool_id === 'string' ? raw.tool_id : 'current',
        },
      };

    case 'PermissionRequest':
      return { sessionId, event: { kind: 'permissionRequest' } };

    case 'Stop':
      return { sessionId, event: { kind: 'turnEnd' } };

    default:
      return null;
  }
}

export const openrouterProvider: HookProvider = {
  kind: 'hook',
  id: 'openrouter',
  displayName: 'OpenRouter 에이전트',
  protocolVersion: 1,

  normalizeHookEvent,

  installHooks: () => Promise.resolve(),
  uninstallHooks: () => Promise.resolve(),
  areHooksInstalled: () => Promise.resolve(true),

  formatToolStatus,
  permissionExemptTools: new Set(['AskUserQuestion']),
  subagentToolNames: new Set(['Classifier', 'Searcher', 'Drafter', 'Reviewer']),
  readingTools: new Set(['Searcher']),
  terminalNamePrefix: 'openrouter',
};
