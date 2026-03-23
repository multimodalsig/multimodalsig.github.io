// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "About",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "dropdown-themes",
              title: "Themes",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/research/themes/";
              },
            },{id: "dropdown-projects",
              title: "Projects",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/research/projects/";
              },
            },{id: "dropdown-gallery",
              title: "Gallery",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/research/gallery/";
              },
            },{id: "dropdown-teaching",
              title: "Teaching",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/teaching/";
              },
            },{id: "nav-publications",
          title: "Publications",
          description: "Publications from the Multimodal Spatial Imaging Lab. Auto-updated monthly from Semantic Scholar.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-people",
          title: "People",
          description: "Members of the Multimodal Spatial Imaging Lab.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/people/";
          },
        },{id: "nav-facilities",
          title: "Facilities",
          description: "Lab equipment and research facilities.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/facilities/";
          },
        },{id: "nav-news",
          title: "News",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/news/";
          },
        },{id: "dropdown-contact",
              title: "Contact",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/contact/#contact";
              },
            },{id: "dropdown-positions",
              title: "Positions",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/contact/#positions";
              },
            },{id: "books-the-godfather",
          title: 'The Godfather',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/the_godfather/";
            },},{id: "news-we-are-recruiting-msc-and-phd-students-for-fall-2026-contact-dr-lichti-with-your-cv-and-transcripts",
          title: 'We are recruiting MSc and PhD students for Fall 2026. Contact Dr. Lichti...',
          description: "",
          section: "News",},{id: "news-the-multimodal-spatial-imaging-lab-website-is-now-live",
          title: 'The Multimodal Spatial Imaging Lab website is now live.',
          description: "",
          section: "News",},{id: "projects-heritage-documentation",
          title: 'Heritage Documentation',
          description: "Digital preservation of at-risk cultural heritage sites.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/heritage/";
            },},{id: "projects-tls-self-calibration",
          title: 'TLS Self-Calibration',
          description: "Systematic error modelling and self-calibration of terrestrial laser scanners.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/tls_calibration/";
            },},{id: "teachings-data-science-fundamentals",
          title: 'Data Science Fundamentals',
          description: "This course covers the foundational aspects of data science, including data collection, cleaning, analysis, and visualization. Students will learn practical skills for working with real-world datasets.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/data-science-fundamentals/";
            },},{id: "teachings-introduction-to-machine-learning",
          title: 'Introduction to Machine Learning',
          description: "This course provides an introduction to machine learning concepts, algorithms, and applications. Students will learn about supervised and unsupervised learning, model evaluation, and practical implementations.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/introduction-to-machine-learning/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%64%64%6C%69%63%68%74%69@%75%63%61%6C%67%61%72%79.%63%61", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=rzfKJOIAAAAJ", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/multimodalsig", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
