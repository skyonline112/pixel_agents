import * as fs from 'fs';
import { OpenAI } from 'openai';
import * as os from 'os';
import * as path from 'path';
import * as readline from 'readline';

// Load env variables
let apiKey = process.env.OPENROUTER_API_KEY || '';

if (!apiKey) {
  const possibleEnvPaths = [
    path.join(process.cwd(), '.env'),
    path.join(process.cwd(), '..', '.env'),
    path.join(process.cwd(), '..', '..', '.env'),
    path.join('C:', 'Users', 'ABC', 'Desktop', 'NIA', '260625 6회차', '.env'),
  ];

  for (const envPath of possibleEnvPaths) {
    if (fs.existsSync(envPath)) {
      try {
        const envContent = fs.readFileSync(envPath, 'utf-8');
        const match = envContent.match(/OPENROUTER_API_KEY\s*=\s*(.*)/);
        if (match && match[1]) {
          apiKey = match[1].trim().replace(/['"]/g, '');
          break;
        }
      } catch (e) {
        // ignore
      }
    }
  }
}

if (!apiKey) {
  console.error('\n❌ 에러: OPENROUTER_API_KEY를 찾을 수 없습니다.');
  console.error('해결 방법:');
  console.error('1. 프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 `OPENROUTER_API_KEY=your_key`를 추가하세요.');
  console.error('2. 또는 환경변수로 설정하여 실행해 주세요 (예: `$env:OPENROUTER_API_KEY="your_key"` 또는 `export OPENROUTER_API_KEY="your_key"`).\n');
  process.exit(1);
}


const openai = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: apiKey,
  defaultHeaders: {
    'HTTP-Referer': 'https://github.com/google-deepmind/antigravity',
    'X-Title': 'Civil Complaint Multi-Agent System'
  }
});

const MODEL_NAME = 'google/gemini-2.5-flash';

// Fetch Pixel Agents Server config
function getServerConfig() {
  const serverJsonPath = path.join(os.homedir(), '.pixel-agents', 'server.json');
  if (!fs.existsSync(serverJsonPath)) {
    throw new Error('Pixel Agents server is not running. Please start the Pixel Agents view in VS Code first!');
  }
  return JSON.parse(fs.readFileSync(serverJsonPath, 'utf-8'));
}

async function postHook(serverConfig: any, sessionId: string, eventName: string, extra: Record<string, any> = {}) {
  const url = `http://127.0.0.1:${serverConfig.port}/api/hooks/openrouter`;
  const body = {
    hook_event_name: eventName,
    session_id: sessionId,
    ...extra
  };
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${serverConfig.token}`
      },
      body: JSON.stringify(body)
    });
    if (!res.ok) {
      console.error(`Hook Delivery Failed: ${res.statusText}`);
    }
  } catch (err) {
    console.error(`Hook Request Error: ${err}`);
  }
}

async function callLLM(systemPrompt: string, userPrompt: string, jsonMode: boolean = false): Promise<string> {
  const response = await openai.chat.completions.create({
    model: MODEL_NAME,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ],
    temperature: 0.2,
    response_format: jsonMode ? { type: 'json_object' } : undefined
  });
  return response.choices[0].message.content?.trim?.() || response.choices[0].message.content || '';
}

// 4 Agents Sessions
const AGENTS = {
  KIM: { id: 'session-kim', name: '김순경' },   // Classifier
  PARK: { id: 'session-park', name: '박경장' }, // Searcher
  CHOI: { id: 'session-choi', name: '최경사' }, // Drafter
  YOO: { id: 'session-yoo', name: '유총경' }    // Reviewer
};

async function runWorkflow() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.question('민원 내용 또는 질문을 입력하세요: ', async (userInput) => {
    rl.close();
    if (!userInput.trim()) {
      console.log('질문이 입력되지 않았습니다. 종료합니다.');
      return;
    }

    let serverConfig;
    try {
      serverConfig = getServerConfig();
    } catch (err: any) {
      console.error(err.message);
      return;
    }

    console.log('\n--- 👮 경찰서 멀티 에이전트 시스템 가동 ---');
    console.log('김순경, 박경장, 최경사, 유총경 에이전트가 픽셀 오피스에 배치됩니다.');

    // Step 0: Initialize sessions for all 4 agents so they sit at desks
    for (const agent of Object.values(AGENTS)) {
      await postHook(serverConfig, agent.id, 'SessionStart', { cwd: process.cwd() });
      // Emit Stop initially so they appear idle
      await postHook(serverConfig, agent.id, 'Stop');
    }

    // Step 1: 김순경 (Classifier) - 분석 및 카테고리 분류
    console.log('\n[김순경] 민원 내용을 분류하고 있습니다...');
    await postHook(serverConfig, AGENTS.KIM.id, 'PreToolUse', {
      tool_name: 'Classifier',
      tool_id: 'tool-kim-1'
    });

    const kimSystem = `당신은 경찰 민원 분석을 담당하는 '김순경'입니다. 
    전달된 민원 주제를 분석하고 카테고리("형사", "교통", "일반행정", "민원신고") 중 하나로 분류하고 3줄 이내로 사유를 작성하여 응답하십시오.`;
    const classification = await callLLM(kimSystem, userInput);
    
    await new Promise(resolve => setTimeout(resolve, 2000)); // styling delay
    await postHook(serverConfig, AGENTS.KIM.id, 'PostToolUse', { tool_id: 'tool-kim-1' });
    await postHook(serverConfig, AGENTS.KIM.id, 'Stop');
    console.log(`[김순경 분류 결과]:\n${classification}`);

    // Step 2: 박경장 (Searcher) - 법령/규정 검색
    console.log('\n[박경장] 유관 법령 및 업무 규정을 검색 중입니다...');
    await postHook(serverConfig, AGENTS.PARK.id, 'PreToolUse', {
      tool_name: 'Searcher',
      tool_id: 'tool-park-1'
    });

    const parkSystem = `당신은 경찰 행정 지식과 법규를 찾아주는 '박경장'입니다. 
    이전 민원 분류 및 내용에 적용될 수 있는 경찰 관련 법률 조항이나 행정 지침을 3가지 찾아서 목록 형태로 작성해 주십시오. 
    절대 답변은 쓰지 마시고 사실 규정만 명시하십시오.`;
    const searchResults = await callLLM(parkSystem, `민원내용: ${userInput}\n분류결과: ${classification}`);

    await new Promise(resolve => setTimeout(resolve, 2000));
    await postHook(serverConfig, AGENTS.PARK.id, 'PostToolUse', { tool_id: 'tool-park-1' });
    await postHook(serverConfig, AGENTS.PARK.id, 'Stop');
    console.log(`[박경장 검색 결과]:\n${searchResults}`);

    // Step 3: 최경사 (Drafter) - 초안 작성
    console.log('\n[최경사] 공식 민원 답변 초안을 작성 중입니다...');
    await postHook(serverConfig, AGENTS.CHOI.id, 'PreToolUse', {
      tool_name: 'Drafter',
      tool_id: 'tool-choi-1'
    });

    const choiSystem = `당신은 공무원 답변을 격식 있게 작성하는 '최경사'입니다. 
    제시된 법령 자료를 기반으로 민원인에게 제공할 친절하고 정중한 답변 초안을 작성하십시오.`;
    const draft = await callLLM(choiSystem, `민원내용: ${userInput}\n검색법규: ${searchResults}`);

    await new Promise(resolve => setTimeout(resolve, 2000));
    await postHook(serverConfig, AGENTS.CHOI.id, 'PostToolUse', { tool_id: 'tool-choi-1' });
    await postHook(serverConfig, AGENTS.CHOI.id, 'Stop');
    console.log(`[최경사 작성 답변 초안]:\n${draft}`);

    // Step 4: 유총경 (Reviewer) - 최종 검수
    console.log('\n[유총경] 답변 초안의 완성도를 검수하고 있습니다...');
    await postHook(serverConfig, AGENTS.YOO.id, 'PreToolUse', {
      tool_name: 'Reviewer',
      tool_id: 'tool-yoo-1'
    });

    const yooSystem = `당신은 최종 검수를 담당하는 경찰서장 '유총경'입니다. 
    최경사가 작성한 초안이 민원인에게 보내기에 격식 있고 정확한지 검토하고, "검수 결과: [승인]" 혹은 수정 요구사항 피드백을 한글로 작성해 주십시오.`;
    const review = await callLLM(yooSystem, `최종초안:\n${draft}`);

    await new Promise(resolve => setTimeout(resolve, 2000));
    await postHook(serverConfig, AGENTS.YOO.id, 'PostToolUse', { tool_id: 'tool-yoo-1' });
    await postHook(serverConfig, AGENTS.YOO.id, 'Stop');
    console.log(`[유총경 최종 검수 코멘트]:\n${review}`);

    console.log('\n==============================================');
    console.log('🎉 모든 경찰 에이전트 협업 완료!');
    console.log('==============================================');

    // Close sessions gracefully after a short delay
    setTimeout(async () => {
      for (const agent of Object.values(AGENTS)) {
        await postHook(serverConfig, agent.id, 'SessionEnd');
      }
      console.log('에이전트 세션이 무사히 종료되었습니다.');
    }, 5000);
  });
}

runWorkflow().catch(console.error);
