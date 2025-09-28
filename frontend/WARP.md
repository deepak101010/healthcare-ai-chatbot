# Development Guide

Essential development guidance for the Healthcare AI Chatbot frontend.

## 🚨 Critical Issues Prevention

### CSS Syntax Validation
**ALWAYS validate CSS before committing:**
- Check all opening braces `{` have matching closing braces `}`
- Ensure all CSS properties end with semicolons `;`
- Verify no orphaned keyframe rules without parent `@keyframes`
- Test compilation with `npm start` immediately after CSS changes

### TypeScript Configuration
- Strict type checking is enabled
- All interfaces must be properly defined
- No implicit `any` types allowed
- React props must be properly typed

### Common Issues & Solutions

#### 1. CSS Compilation Error
**Symptoms**: White screen, console errors about CSS
**Solution**: 
```bash
# Check App.css for syntax errors
# Look for missing semicolons, unmatched braces
# Validate @keyframes and @media queries
```

#### 2. Backend Connection Issues
**Symptoms**: "Network Error" or CORS issues
**Solution**:
- Ensure backend is running on port 8000
- Check `API_BASE_URL` in App.tsx
- Verify CORS settings in backend

#### 3. TypeScript Errors
**Symptoms**: Red underlines, build failures
**Solution**:
- Check interface definitions
- Ensure all props are properly typed
- Use proper React.FC<> types for components

#### 4. Dependencies Issues
**Symptoms**: Module not found errors
**Solution**:
```bash
npm install  # Install missing dependencies
npm audit    # Check for vulnerabilities
```

## 🔧 Quick Commands

### Development
```bash
npm install     # Install dependencies
npm start       # Start development server (http://localhost:3000)
npm test        # Run tests
npm run build   # Production build
```

### Debugging
```bash
npm cache clean --force    # Clear npm cache
rm -rf node_modules && npm install  # Reinstall everything
```

## 🏗️ Architecture Notes

### File Structure
```
frontend/src/
├── App.tsx          # Main React component with chat interface
├── App.css          # Healthcare-focused styling (CRITICAL - syntax sensitive)
├── index.tsx        # React entry point
└── react-app-env.d.ts  # TypeScript declarations
```

### Key Components

#### App.tsx
- Main chat interface component
- Handles state management for messages
- Integrates with backend API via axios
- Implements real-time chat functionality

#### App.css
- **CRITICAL**: Must be syntactically perfect
- Healthcare color scheme with gradients
- Responsive design for mobile/desktop
- Smooth animations and transitions
- Custom scrollbar styling

### State Management
```typescript
interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  severity?: string;
}
```

## 🎨 Styling Guidelines

### Color Palette
- Primary: `#667eea` (medical blue)
- Secondary: `#764ba2` (professional purple)  
- Success/Mild: `#2196F3` (light blue)
- Warning/Serious: `#f44336` (medical red)
- Background: `#f7f7f8` (clean gray)

### Component Classes
- `.chat-container` - Main chat wrapper
- `.message` - Individual message wrapper
- `.user-message` - User's messages (right-aligned)
- `.bot-message` - AI responses (left-aligned)
- `.serious-message` - Urgent medical warnings
- `.typing-indicator` - Loading animation

### Responsive Breakpoints
- Desktop: Default styling
- Mobile: `@media (max-width: 768px)`

## 🧪 Testing Checklist

### Before Committing
- [ ] CSS compiles without errors (`npm start`)
- [ ] TypeScript builds successfully
- [ ] No console errors in browser
- [ ] Chat functionality works end-to-end
- [ ] Responsive design works on mobile
- [ ] All animations play smoothly

### Manual Testing
1. **Load Application**: Should show welcome message
2. **Send Message**: Type symptoms, click Send
3. **Receive Response**: Should get AI response with severity
4. **Error Handling**: Stop backend, should show error
5. **Mobile View**: Test on different screen sizes

## 🚨 Critical Code Areas

### App.tsx Line 62-64
```typescript
const response = await axios.post<ApiResponse>(`${API_BASE_URL}/diagnose`, {
  symptoms: inputValue
});
```
**Note**: This is the main API integration point

### App.css Lines 149-158
```css
@keyframes typing {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}
```
**Note**: Critical animation - ensure proper syntax

## 🔄 Hot Reload Configuration

The app uses Create React App's built-in hot reload:
- Changes to `.tsx` files reload automatically
- Changes to `.css` files update styles instantly
- TypeScript errors appear in browser overlay

## 📱 Mobile Considerations

- Font size increased to 16px on mobile (prevents zoom)
- Touch-friendly button sizes (44px minimum)
- Proper viewport meta tag configured
- Smooth scroll behavior on iOS/Android

## 🛡️ Security Notes

- No sensitive data stored in frontend
- API key handled only by backend
- Proper CORS configuration required
- Input sanitization handled by backend

## 📝 Development Workflow

1. **Start Development**: `npm start`
2. **Make Changes**: Edit files in `src/`
3. **Test Locally**: Verify functionality
4. **Check TypeScript**: Fix any type errors
5. **Validate CSS**: Ensure no syntax issues
6. **Test Mobile**: Check responsive design
7. **Commit**: Only after all tests pass

---

**Remember**: This is a healthcare application - prioritize user safety and data accuracy in all development decisions.