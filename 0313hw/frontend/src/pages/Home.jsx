import { useState } from 'react';
import { api } from '@utils/network.js'

const Home = () => {
  const [messages, setMessages] = useState([
    { role: 'bot', content: '안녕하세요! 무엇을 도와드릴까요?' },
    // { role: 'user', content: '리액트로 채팅 UI 만드는 법 알려줘.' },
    // { role: 'bot', content: '부트스트랩의 flex 클래스를 활용하면 말풍선을 쉽게 정렬할 수 있어요!' }
    
  ]);
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');

  const Send = () => {
    api.get("/webhook/app", { params: {"input": input} })
    .then(res => {
      // console.log(res)
      if (res.data && res.data.content) {
          setMessages(prev => [...prev, { 
            role: 'bot', 
            content: res.data.content 
          }])}
    })
    .catch(err => {
      console.log(err)
    })

    if (!input.trim()) return;
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');

    // 응답 시뮬레이션
    // setTimeout(() => {
    //   setMessages(prev => [...prev, { 
    //     role: 'bot', 
    //     content: output 
    //   }]);
    // }, 800);
  };

  return (
    <div className="container-fluid vh-100 d-flex flex-column bg-white">
      {/* 헤더 */}
      <header className="p-3 border-bottom bg-white sticky-top">
        <h5 className="mb-0 fw-bold text-primary">YW Chat</h5>
      </header>

      {/* 채팅 내역 (말풍선 영역) */}
      <div className="flex-grow-1 overflow-auto p-4 bg-light">
        <div className="container" style={{ maxWidth: '700px' }}>
          {messages.map((msg, idx) => (
            <div key={idx} className={`d-flex mb-4 ${msg.role === 'user' ? 'justify-content-end' : 'justify-content-start'}`}>
              
              {/* AI 아이콘 (왼쪽 답변일 때만 표시) */}
              {msg.role === 'bot' && (
                <div className="me-2 mt-1">
                  <div className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center" style={{ width: '30px', height: '30px', fontSize: '12px' }}>
                    AI
                  </div>
                </div>
              )}

              {/* 말풍선 본체 */}
              <div 
                className={`p-3 shadow-sm ${
                  msg.role === 'user' 
                    ? 'bg-primary text-white rounded-start-4 rounded-top-4' // 사용자
                    : 'bg-white text-dark border rounded-end-4 rounded-top-4' // AI
                }`}
                style={{ maxWidth: '75%', fontSize: '0.95rem' }}
              >
                <div className="fw-bold mb-1 small" style={{ opacity: 0.8 }}>
                  {msg.role === 'user' ? '나' : 'Gemini'}
                </div>
                <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 입력창 */}
      <div className="p-3 border-top bg-white">
        <div className="container" style={{ maxWidth: '700px' }}>
          <div className="input-group border rounded-pill px-3 py-1 shadow-sm">
            <input 
              type="text" 
              className="form-control border-0 shadow-none" 
              placeholder="메시지를 입력하세요..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && Send()}
            />
            <button className="btn btn-link text-primary fw-bold text-decoration-none" onClick={Send}>
              전송
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;