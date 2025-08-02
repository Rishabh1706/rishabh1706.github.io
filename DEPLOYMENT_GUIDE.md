# Portfolio Deployment Guide

## Option 1: Azure Static Web Apps (FREE)

### Prerequisites
- Azure account (free tier available)
- GitHub account
- Your portfolio files

### Steps

1. **Create GitHub Repository**
   ```bash
   # In your portfolio folder
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/portfolio.git
   git push -u origin main
   ```

2. **Deploy to Azure Static Web Apps**
   - Go to [Azure Portal](https://portal.azure.com)
   - Search "Static Web Apps" → Create
   - Choose "Free" plan
   - Connect to your GitHub repository
   - Build settings:
     - App location: `/`
     - Output location: `/`
   - Azure will create GitHub Actions for auto-deployment

3. **Custom Domain (Optional)**
   - In Azure portal → Your Static Web App → Custom domains
   - Add your domain and follow DNS configuration

### Cost: **FREE** ✅

---

## Option 2: Netlify (Easy Form Handling)

### Steps

1. **Prepare for Netlify**
   - Your form is already configured with `data-netlify="true"`
   - Create account at [netlify.com](https://netlify.com)

2. **Deploy Options**

   **Option A: Drag & Drop**
   - Zip your portfolio folder
   - Drag to Netlify dashboard
   - Instant deployment!

   **Option B: GitHub Integration**
   - Connect GitHub repository
   - Auto-deploy on git push

3. **Form Setup**
   - Forms → Form notifications
   - Add your email: `rishabhgupta1706@gmail.com`
   - You'll receive submissions in your inbox!

### Cost: **FREE** (100 form submissions/month) ✅

---

## Option 3: Azure Functions + SendGrid (Advanced)

### For Custom Email Handling

```javascript
// Azure Function (index.js)
const sgMail = require('@sendgrid/mail');

module.exports = async function (context, req) {
    sgMail.setApiKey(process.env.SENDGRID_API_KEY);
    
    const { name, email, subject, message } = req.body;
    
    const msg = {
        to: 'rishabhgupta1706@gmail.com',
        from: 'noreply@yourportfolio.com', // Verified sender
        subject: `Portfolio Contact: ${subject}`,
        html: `
            <h3>New message from ${name}</h3>
            <p><strong>Email:</strong> ${email}</p>
            <p><strong>Subject:</strong> ${subject}</p>
            <p><strong>Message:</strong></p>
            <p>${message}</p>
        `
    };
    
    try {
        await sgMail.send(msg);
        context.res = {
            status: 200,
            body: { success: true }
        };
    } catch (error) {
        context.res = {
            status: 500,
            body: { error: 'Failed to send email' }
        };
    }
};
```

### SendGrid Setup
- Free tier: 100 emails/day
- Verify sender domain
- Get API key

### Cost: **~$2-5/month** (depending on usage)

---

## Recommendation

**For your use case, I recommend:**

1. **Netlify** - Easiest setup, built-in form handling
2. **Azure Static Web Apps** - If you prefer Azure ecosystem

Both options are **FREE** and will handle your contact form perfectly!

## Quick Start Commands

```bash
# Option 1: Quick Netlify deployment
npx netlify-cli deploy --prod --dir .

# Option 2: Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli
swa deploy --env production
```

## Security Notes

- Both platforms provide HTTPS automatically
- Form spam protection included
- No server maintenance required
- Global CDN for fast loading

Your portfolio will be live in minutes! 🚀
