import React from 'react';

interface StarterPromptsProps {
  onSelectPrompt: (prompt: string) => void;
}

const prompts = [
  {
    icon: '🏖️',
    title: 'Beach Vacation',
    prompt: "I'd like to plan a relaxing beach vacation for 7 days with my family",
  },
  {
    icon: '🏔️',
    title: 'Adventure Trip',
    prompt: "I'm looking for an adventurous trip with hiking and outdoor activities",
  },
  {
    icon: '🏛️',
    title: 'Cultural Experience',
    prompt: "I want to explore historical sites and immerse myself in local culture",
  },
  {
    icon: '🍷',
    title: 'Food & Wine',
    prompt: "I'm interested in a culinary journey with great restaurants and wine tasting",
  },
];

export default function StarterPrompts({ onSelectPrompt }: StarterPromptsProps) {
  return (
    <div className="grid grid-cols-2 gap-3 p-4">
      <p className="col-span-2 text-sm text-gray-600 mb-2">
        Try one of these to get started:
      </p>
      {prompts.map((prompt, index) => (
        <button
          key={index}
          onClick={() => onSelectPrompt(prompt.prompt)}
          className="flex items-start space-x-3 p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors text-left"
        >
          <span className="text-2xl">{prompt.icon}</span>
          <div>
            <p className="font-medium text-sm text-gray-900">{prompt.title}</p>
            <p className="text-xs text-gray-600 mt-1">{prompt.prompt}</p>
          </div>
        </button>
      ))}
    </div>
  );
}