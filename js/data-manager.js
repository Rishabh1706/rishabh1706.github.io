// Data Manager - Handles loading and caching of JSON data
class DataManager {
    constructor() {
        this.cache = {};
        this.baseUrl = './data/';
    }

    async loadData(filename) {
        if (this.cache[filename]) {
            return this.cache[filename];
        }

        try {
            const response = await fetch(`${this.baseUrl}${filename}`);
            if (!response.ok) {
                throw new Error(`Failed to load ${filename}: ${response.statusText}`);
            }
            const data = await response.json();
            this.cache[filename] = data;
            return data;
        } catch (error) {
            console.error(`Error loading ${filename}:`, error);
            return null;
        }
    }

    async getAllData() {
        const [experience, projects, education, profile] = await Promise.all([
            this.loadData('experience.json'),
            this.loadData('projects.json'),
            this.loadData('education.json'),
            this.loadData('profile.json')
        ]);

        return { experience, projects, education, profile };
    }
}

// Experience Renderer
class ExperienceRenderer {
    constructor(data) {
        this.data = data;
    }

    renderExperience() {
        const timeline = document.querySelector('.timeline');
        if (!timeline || !this.data.experience) return;

        timeline.innerHTML = this.data.experience.map(exp => this.createExperienceItem(exp)).join('');
    }

    createExperienceItem(exp) {
        const logoHtml = exp.logo === 'custom-gradient' 
            ? `<div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 14px;">${exp.logoText}</div>`
            : `<img src="${exp.logo}" alt="${exp.company}" style="width: 40px; height: 40px; object-fit: contain;">`;

        const skillsHtml = exp.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('');

        return `
            <div class="timeline-item">
                <div class="timeline-date">${exp.startDate} - ${exp.endDate}</div>
                <div class="timeline-content">
                    <div class="company-header">
                        <div class="company-logo">
                            ${logoHtml}
                        </div>
                        <div class="company-info">
                            <h3 class="company-name">${exp.company}</h3>
                            <h4 class="job-title">${exp.position}</h4>
                        </div>
                    </div>
                    <p>${exp.description}</p>
                    <div class="timeline-skills">
                        ${skillsHtml}
                    </div>
                </div>
            </div>
        `;
    }
}

// Projects Renderer
class ProjectsRenderer {
    constructor(data) {
        this.data = data;
    }

    renderProjects() {
        const projectsGrid = document.querySelector('.projects-grid');
        if (!projectsGrid || !this.data.projects) return;

        projectsGrid.innerHTML = this.data.projects.map(project => this.createProjectCard(project)).join('');
    }

    createProjectCard(project) {
        const techTags = project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('');
        const stats = project.stats.map(stat => `<span><i class="${stat.icon}"></i> ${stat.text}</span>`).join('');

        return `
            <div class="project-card ${project.featured ? 'featured' : ''}">
                <div class="project-image">
                    <div class="project-overlay">
                        <div class="project-links">
                            <a href="${project.links.demo}" class="project-link"><i class="fas fa-external-link-alt"></i></a>
                            <a href="${project.links.github}" class="project-link"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                    <div class="project-tech-stack">
                        ${techTags}
                    </div>
                    <div class="project-icon">
                        <img src="${project.icon}" alt="${project.title}" style="width: 60px; height: 60px;">
                    </div>
                </div>
                <div class="project-content">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <div class="project-stats">
                        ${stats}
                    </div>
                </div>
            </div>
        `;
    }
}

// Education Renderer
class EducationRenderer {
    constructor(data) {
        this.data = data;
    }

    renderEducation() {
        this.renderEducationCards();
        this.renderCertifications();
    }

    renderEducationCards() {
        const educationGrid = document.querySelector('.education-grid');
        if (!educationGrid || !this.data.education) return;

        educationGrid.innerHTML = this.data.education.map(edu => this.createEducationCard(edu)).join('');
    }

    createEducationCard(edu) {
        const skillsHtml = edu.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('');

        return `
            <div class="education-card">
                <div class="education-icon">
                    <img src="${edu.logo}" alt="${edu.institution}" style="width: 80px; height: 80px; object-fit: contain;">
                </div>
                <div class="education-content">
                    <h3>${edu.degree}</h3>
                    <h4>${edu.field}</h4>
                    <p class="institution">${edu.institution} • ${edu.year}</p>
                    <p class="description">${edu.description}</p>
                    <div class="education-skills">
                        ${skillsHtml}
                    </div>
                </div>
            </div>
        `;
    }

    renderCertifications() {
        const certificationsGrid = document.querySelector('.certifications-grid');
        if (!certificationsGrid || !this.data.certifications) return;

        certificationsGrid.innerHTML = this.data.certifications.map(cert => this.createCertificationCard(cert)).join('');
    }

    createCertificationCard(cert) {
        return `
            <div class="cert-card" style="background: white; padding: 1.5rem; border-radius: var(--border-radius); box-shadow: var(--shadow-md); text-align: center; transition: var(--transition);">
                <i class="${cert.icon}" style="font-size: 2rem; color: var(--primary-color); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">${cert.name}</h4>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">${cert.fullName}</p>
                <div style="margin-top: 1rem; font-size: 0.8rem; color: var(--text-light);">
                    <span>${cert.issuer} • ${cert.date}</span>
                </div>
            </div>
        `;
    }
}

// Profile Renderer
class ProfileRenderer {
    constructor(data) {
        this.data = data;
    }

    renderProfile() {
        if (!this.data.profile) return;

        this.updateHeroSection();
        this.updateAboutSection();
        this.updateContactSection();
    }

    updateHeroSection() {
        const profile = this.data.profile.personal;
        
        // Update typing text
        const typingText = document.querySelector('.typing-text');
        if (typingText) typingText.textContent = profile.title;

        // Update subtitle
        const subtitle = document.querySelector('.hero-subtitle');
        if (subtitle) subtitle.textContent = profile.subtitle;

        // Update description
        const description = document.querySelector('.hero-description');
        if (description) description.textContent = profile.description;

        // Update profile photo
        const profileImg = document.querySelector('.profile-img');
        if (profileImg && profile.photo) {
            profileImg.src = profile.photo;
            profileImg.alt = profile.name;
        }

        // Update resume download button
        const resumeBtn = document.querySelector('.download-resume');
        if (resumeBtn && this.data.profile.resumeUrl) {
            resumeBtn.href = this.data.profile.resumeUrl;
            resumeBtn.style.display = 'inline-flex';
        } else if (resumeBtn) {
            resumeBtn.style.display = 'none';
        }
    }

    updateAboutSection() {
        const about = this.data.profile.about;
        const personal = this.data.profile.personal;
        
        // Update about text
        const aboutTitle = document.querySelector('.about-text h3');
        if (aboutTitle) aboutTitle.textContent = about.title;

        const aboutDesc = document.querySelector('.about-text p');
        if (aboutDesc) aboutDesc.textContent = about.description;

        // Update about photo
        const aboutImg = document.querySelector('.about-profile-img');
        if (aboutImg && personal.photo) {
            aboutImg.src = personal.photo;
            aboutImg.alt = personal.name + ' - About';
        }

        // Update stats
        about.stats.forEach((stat, index) => {
            const statNumber = document.querySelector(`.stat-item:nth-child(${index + 1}) .stat-number`);
            const statLabel = document.querySelector(`.stat-item:nth-child(${index + 1}) .stat-label`);
            
            if (statNumber) statNumber.setAttribute('data-target', stat.number);
            if (statLabel) statLabel.textContent = stat.label;
        });
    }

    updateContactSection() {
        const contact = this.data.profile.contact;
        const personal = this.data.profile.personal;

        // Update contact info
        const contactTitle = document.querySelector('.contact-info h3');
        if (contactTitle) contactTitle.textContent = contact.title;

        const contactDesc = document.querySelector('.contact-info p');
        if (contactDesc) contactDesc.textContent = contact.description;

        // Update contact details
        const emailSpan = document.querySelector('.contact-item .fas.fa-envelope').nextElementSibling;
        if (emailSpan) emailSpan.textContent = personal.email;

        const phoneSpan = document.querySelector('.contact-item .fas.fa-phone').nextElementSibling;
        if (phoneSpan) phoneSpan.textContent = personal.phone;

        const locationSpan = document.querySelector('.contact-item .fas.fa-map-marker-alt').nextElementSibling;
        if (locationSpan) locationSpan.textContent = personal.location;
    }
}

// Main Application
class PortfolioApp {
    constructor() {
        this.dataManager = new DataManager();
        this.init();
    }

    async init() {
        try {
            // Show loading state
            this.showLoading();

            // Load all data
            const data = await this.dataManager.getAllData();

            // Initialize renderers
            const experienceRenderer = new ExperienceRenderer(data);
            const projectsRenderer = new ProjectsRenderer(data);
            const educationRenderer = new EducationRenderer(data);
            const profileRenderer = new ProfileRenderer(data);

            // Render all sections
            profileRenderer.renderProfile();
            experienceRenderer.renderExperience();
            projectsRenderer.renderProjects();
            educationRenderer.renderEducation();

            // Hide loading state
            this.hideLoading();

            console.log('Portfolio loaded successfully!');
        } catch (error) {
            console.error('Failed to load portfolio:', error);
            this.showError();
        }
    }

    showLoading() {
        // You can add a loading spinner here
        console.log('Loading portfolio data...');
    }

    hideLoading() {
        // Hide loading spinner
        console.log('Portfolio data loaded!');
    }

    showError() {
        console.error('Failed to load portfolio data');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PortfolioApp();
});

// Export for module usage (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PortfolioApp, DataManager };
}
