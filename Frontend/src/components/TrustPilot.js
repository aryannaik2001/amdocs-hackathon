import React, { useState } from 'react';
import { Flag, Info, Maximize2, X } from 'lucide-react';

const TrustPilot = () => {
  const [selectedPlatform, setSelectedPlatform] = useState('x');
  const [factCheckInput, setFactCheckInput] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const posts = [
    { id: 1, username: '@elonmusk', time: '2 minutes ago', truth: 80, text: 'Extremely concerning.NED is RIFE with CORRUPTION!! What is going on here?  @SenToddYoung' },
    { id: 2, username: '@elonmusk', time: '5 minutes ago', truth: 68, text: 'Tax regulations need a massive reset. They are torturing the American people!' },
    { id: 3, username: '@elonmusk', time: '10 minutes ago', truth: 50, text: 'Americans are excited about the future and love what President @realDonaldTrump is getting done!' },
  ];

//   const handleFactCheck = async () => {
//     if (!factCheckInput.trim()) return;
    
//     setIsLoading(true);
//     try {
//       const response = await fetch('http://localhost:8000/analyze', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'Accept': 'application/json',
//         },
//         body: JSON.stringify({
//           text: factCheckInput
//         }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to analyze text');
//       }

//       const data = await response.json();
//       setAnalysisResult(data);
//     } catch (error) {
//       console.error('Error:', error);
//     } finally {
//       setIsLoading(false);
//     }
//   };

const handleFactCheck = async () => {
    if (!factCheckInput.trim()) return;
    
    setIsLoading(true);
    try {
      console.log('Sending request to analyze:', factCheckInput);
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          text: factCheckInput
        }),
      });

      console.log('Response status:', response.status);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`Failed to analyze text: ${errorText}`);
      }

      const data = await response.json();
      console.log('Received data:', data);
      setAnalysisResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
    };









    
  return (
    <div className="max-w-6xl mx-auto p-4 bg-gray-50 min-h-screen">
      <nav className="flex justify-between items-center p-4 bg-white rounded-lg mb-4">
        <div className="flex items-center gap-2">
          <div className="text-purple-600 font-bold text-xl">Trust Pilot</div>
        </div>
        <div className="flex gap-4">
          <button className="px-4 py-2 hover:bg-gray-100 rounded">Home</button>
          <button className="px-4 py-2 hover:bg-gray-100 rounded">Real-Time Feed</button>
          <button className="px-4 py-2 hover:bg-gray-100 rounded">Reports</button>
          <button className="px-4 py-2 hover:bg-gray-100 rounded">Extension</button>
          <button className="px-4 py-2 hover:bg-gray-100 rounded">Settings</button>
        </div>
      </nav>

      <div className="grid grid-cols-4 gap-4">
        <div className="col-span-1">
          <div className="space-y-2">
            <button 
              className={`w-full p-3 rounded-lg flex items-center gap-2 ${
                selectedPlatform === 'x' ? 'bg-gray-200' : 'bg-white'
              }`}
              onClick={() => setSelectedPlatform('x')}
            >
              <X size={20} />
              Currently viewing
            </button>

            <button 
              className={`w-full p-3 rounded-lg flex items-center gap-2 ${
                selectedPlatform === 'reddit' ? 'bg-gray-200' : 'bg-white'
              }`}
              onClick={() => setSelectedPlatform('reddit')}
            >
              <div className="text-orange-500">
                <svg viewBox="0 0 20 20" className="w-5 h-5">
                  <circle cx="10" cy="10" r="10" fill="currentColor"/>
                </svg>
              </div>
              Switch to Image detection
            </button>
            
            <button 
              className={`w-full p-3 rounded-lg flex items-center gap-2 ${
                selectedPlatform === 'reddit' ? 'bg-gray-200' : 'bg-white'
              }`}
              onClick={() => setSelectedPlatform('reddit')}
            >
              <div className="text-orange-500">
                <svg viewBox="0 0 20 20" className="w-5 h-5">
                  <circle cx="10" cy="10" r="10" fill="currentColor"/>
                </svg>
              </div>
              Switch to Reddit
            </button>

            
            
            <button 
              className={`w-full p-3 rounded-lg flex items-center gap-2 ${
                selectedPlatform === 'facebook' ? 'bg-gray-200' : 'bg-white'
              }`}
              onClick={() => setSelectedPlatform('facebook')}
            >
              <div className="text-blue-600">
                <svg viewBox="0 0 20 20" className="w-5 h-5">
                  <rect width="20" height="20" rx="4" fill="currentColor"/>
                </svg>
              </div>
              Switch to Facebook
            </button>
          </div>
        </div>

       

        <div className="col-span-2">
          <div className="bg-white p-4 rounded-lg mb-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Real Time Feed - X</h2>
              <div className="flex gap-2">
                <button className="p-2 hover:bg-gray-100 rounded"><Maximize2 size={20} /></button>
                <button className="p-2 hover:bg-gray-100 rounded"><X size={20} /></button>
              </div>
            </div>
            
            <div className="space-y-4">
              {posts.map(post => (
                <div key={post.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center gap-2">
                      <div />
                      <div>
                        <div className="font-semibold">{post.username}</div>
                        <div className="text-sm text-gray-500">{post.time}</div>
                      </div>
                    </div>
                    <span className={`px-2 py-1 rounded ${
                      post.truth >= 70 ? 'bg-green-100 text-green-700' :
                      post.truth >= 30 ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {post.truth}% True
                    </span>
                  </div>
                  <p className="text-gray-700">{post.text}</p>
                  <button className="text-sm text-gray-500 mt-2 flex items-center gap-1">
                    <Flag size={16} />
                    Flag Details
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">Fact Checker</h2>
            <div className="flex gap-2 mb-4">
              <input
                type="text"
                className="flex-1 p-2 border rounded"
                placeholder="Enter claim to fact-check..."
                value={factCheckInput}
                onChange={(e) => setFactCheckInput(e.target.value)}
              />
              <button 
                className={`px-4 py-2 bg-purple-100 text-purple-700 rounded hover:bg-purple-200 ${
                  isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
                onClick={handleFactCheck}
                disabled={isLoading}
              >
                {isLoading ? 'Checking...' : 'Check'}
              </button>
            </div>
            
            <div className="bg-gray-50 p-4 rounded">
              <div className="flex justify-between items-center mb-2">
                <div className="font-semibold">Source: Fact Check Organization</div>
                <div className="text-green-700">Trust Rating: 95%</div>
              </div>
              <div className="text-gray-700 mb-4">Fact check result details...</div>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center gap-1">
                  <Info size={16} />
                  "Sources Verified" – Shows a list of credible sources.
                </div>
                <div className="flex items-center gap-1">
                  <Info size={16} />
                  "Flagged Reasons" – Explains why the content is suspicious.
                </div>
                <div className="flex items-center gap-1">
                  <Info size={16} />
                  "Similar Claims" – Links to related, verified content.
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-span-1">
          <div className="bg-white p-4 rounded-lg">
            {analysisResult ? (
              <>
                <div className="flex justify-between items-center mb-4">
                  <div className="text-2xl font-bold">
                    {Math.round(analysisResult.confidence * 100)}%
                  </div>
                  <div className="flex gap-2">
                    <button className="p-1 hover:bg-gray-100 rounded"><Maximize2 size={16} /></button>
                    <button className="p-1 hover:bg-gray-100 rounded"><X size={16} /></button>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <div className="text-gray-700 mb-1">
                      Reliability Status: {analysisResult.credibility_level.replace('_', ' ')}
                    </div>
                    <div className="text-gray-700 mb-2">
                      Confidence Score: {(analysisResult.confidence * 100).toFixed(1)}%
                    </div>
                    <div className="text-gray-700">{analysisResult.evidence[0]}</div>
                  </div>
                  
                  <div className="flex gap-2">
                    <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">
                      Sources Verified
                    </button>
                    <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">
                      Flagged Reasons
                    </button>
                    <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">
                      Similar Claims
                    </button>
                  </div>
                  
                  <div>
                    <div className="text-sm font-semibold mb-1">Sources:</div>
                    <ul className="text-sm text-gray-700 list-disc pl-4">
                      {analysisResult.sources.slice(0, 2).map((source, index) => (
                        <li key={index}>{new URL(source).hostname}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </>
            ) : (
              <>
                <div className="flex justify-between items-center mb-4">
                  <div className="text-2xl font-bold">80%</div>
                  <div className="flex gap-2">
                    <button className="p-1 hover:bg-gray-100 rounded"><Maximize2 size={16} /></button>
                    <button className="p-1 hover:bg-gray-100 rounded"><X size={16} /></button>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <div className="text-gray-700 mb-1">Reliability Status: Likely True</div>
                    <div className="text-gray-700 mb-2">Confidence Score: 89%</div>
                    <div className="text-gray-700">This claim is supported by credible medical research.</div>
                  </div>
                  
                  <div className="flex gap-2">
                    <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">Sources Verified</button>
                    <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">Flagged Reasons</button>
                    <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">Similar Claims</button>
                  </div>
                  
                  <div>
                    <div className="text-sm font-semibold mb-1">Sources:</div>
                    <ul className="text-sm text-gray-700 list-disc pl-4">
                      <li>ABC</li>
                      <li>XYZ</li>
                    </ul>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrustPilot;

