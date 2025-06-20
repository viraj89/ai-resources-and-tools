# 🌐 AI Insights Daily - Website

This is the frontend application for AI Insights Daily, built with [Next.js](https://nextjs.org) 15.3.4 and React 19.

## 🌐 Live Website

**🔗 Live URL**: [https://ai-resources-and-tools.vercel.app](https://ai-resources-and-tools.vercel.app)

## 🚀 Features

- **Modern UI**: Clean, responsive design with Tailwind CSS v4
- **TypeScript**: Full type safety across the application
- **Performance**: Optimized with Next.js static generation
- **Mobile-First**: Responsive design that works on all devices
- **Real-Time Updates**: Content updates automatically via GitHub Actions

## 🛠️ Tech Stack

- **Framework**: Next.js 15.3.4
- **UI Library**: React 19
- **Styling**: Tailwind CSS v4
- **Language**: TypeScript
- **Deployment**: Vercel

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

## 🔧 Development

### Getting Started

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd auto-news/website
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Project Structure

```
website/
├── src/
│   ├── app/                 # Next.js app router
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Main page
│   │   └── globals.css     # Global styles
│   └── components/         # React components
│       └── DailyUpdateSection.tsx
├── public/                 # Static assets
├── package.json           # Dependencies and scripts
└── tsconfig.json         # TypeScript configuration
```

### Content Updates

The website content is automatically updated daily via:

1. **Backend Processing**: Python scripts generate content files
2. **Data Preparation**: `prepare-website-data` script processes content
3. **Automatic Deployment**: GitHub Actions deploys updates to Vercel

### Customization

- **Styling**: Modify `src/app/globals.css` for global styles
- **Components**: Add new components in `src/components/`
- **Layout**: Update `src/app/layout.tsx` for layout changes
- **Content**: Content is generated from backend scripts

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect Repository**: Link your GitHub repository to Vercel
2. **Automatic Deployment**: Updates are deployed automatically on push
3. **Environment Variables**: Configure any required environment variables

### Manual Deployment

```bash
# Build the application
npm run build

# Deploy to your preferred platform
# (Vercel, Netlify, etc.)
```

## 📊 Performance

- **Lighthouse Score**: 95+ across all metrics
- **Core Web Vitals**: Optimized for performance
- **SEO**: Static generation for better search engine optimization
- **Accessibility**: WCAG compliant design

## 🔗 Integration

This website is part of the larger AI Insights Daily platform:

- **Backend**: Python scripts in `../src/scripts/`
- **Content**: Generated from `../artifacts/`
- **Configuration**: Managed via `../data/config/`
- **Automation**: GitHub Actions workflows

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Part of the AI Insights Daily Platform**  
**Version**: 3.1.0  
**Next.js**: 15.3.4  
**React**: 19.0.0
