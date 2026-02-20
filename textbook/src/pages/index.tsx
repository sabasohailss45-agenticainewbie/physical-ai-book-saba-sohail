import type { ReactNode } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

interface ModuleCard {
  number: string;
  icon: string;
  title: string;
  description: string;
  link: string;
  color: string;
}

const MODULES: ModuleCard[] = [
  {
    number: 'Module 1',
    icon: '🧠',
    title: 'Foundations of Physical AI',
    description:
      'Discover what Physical AI is, its history from early robots to Tesla Optimus, and why embodiment is fundamental to intelligence.',
    link: '/docs/foundations/intro',
    color: '#1a73e8',
  },
  {
    number: 'Module 2',
    icon: '👁️',
    title: 'Sensing & Perception',
    description:
      'Explore how robots perceive their environment through cameras, LiDAR, IMUs, and tactile sensors — and how they fuse it all together.',
    link: '/docs/sensing/sensors',
    color: '#0b8043',
  },
  {
    number: 'Module 3',
    icon: '⚙️',
    title: 'Actuation & Control',
    description:
      'Dive into actuator technologies, robot kinematics, dynamics, PID control, model-predictive control, and reinforcement learning for locomotion.',
    link: '/docs/actuation/actuators',
    color: '#e37400',
  },
  {
    number: 'Module 4',
    icon: '🤖',
    title: 'Humanoid Robots & Future Directions',
    description:
      'Examine humanoid platforms like Atlas and Optimus, whole-body control, foundation models for robotics, and the ethics of autonomous machines.',
    link: '/docs/humanoids/humanoid-arch',
    color: '#9c27b0',
  },
];

function HeroSection() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={styles.hero}>
      <div className={styles.heroInner}>
        <div className={styles.heroBadge}>📚 Interactive Textbook</div>
        <Heading as="h1" className={styles.heroTitle}>
          {siteConfig.title}
        </Heading>
        <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
        <div className={styles.heroActions}>
          <Link className="button button--primary button--lg" to="/docs/foundations/intro">
            Start Reading →
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="https://github.com/sabasohailss45-agenticainewbie/physical-ai-book-saba-sohail"
          >
            GitHub ⭐
          </Link>
        </div>
      </div>
    </header>
  );
}

function ModuleGrid() {
  return (
    <section className={styles.moduleSection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          Textbook Modules
        </Heading>
        <p className={styles.sectionSubtitle}>
          Four comprehensive modules covering the complete Physical AI stack — from theory to deployment.
        </p>
        <div className={styles.grid}>
          {MODULES.map((mod) => (
            <Link key={mod.number} to={mod.link} className={styles.card}>
              <div className={styles.cardHeader} style={{ borderColor: mod.color }}>
                <span className={styles.cardIcon}>{mod.icon}</span>
                <span className={styles.cardNumber} style={{ color: mod.color }}>
                  {mod.number}
                </span>
              </div>
              <Heading as="h3" className={styles.cardTitle}>
                {mod.title}
              </Heading>
              <p className={styles.cardDescription}>{mod.description}</p>
              <span className={styles.cardCta} style={{ color: mod.color }}>
                Start reading →
              </span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

function ChatCallout() {
  return (
    <section className={styles.chatCallout}>
      <div className="container">
        <div className={styles.chatCalloutInner}>
          <span className={styles.chatCalloutIcon}>🤖</span>
          <div>
            <Heading as="h3" className={styles.chatCalloutTitle}>
              Ask the AI Tutor
            </Heading>
            <p className={styles.chatCalloutText}>
              Have questions while reading? Click the <strong>🤖 button</strong> in the bottom-right
              corner to chat with your AI tutor — powered by GPT-4o-mini with RAG over the textbook content.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="An interactive textbook on Physical AI and humanoid robotics with an embedded RAG chatbot tutor."
    >
      <HeroSection />
      <main>
        <ModuleGrid />
        <ChatCallout />
      </main>
    </Layout>
  );
}
