import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link'; // Import Link

type FeatureItem = {
  title: string;
  description: ReactNode;
  to: string; // Add 'to' property for the link
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Module 1: The Robotic Nervous System (ROS 2)',
    to: '/docs/01-ros2',
    description: (
      <>
        Explore the fundamentals of the Robot Operating System 2, focusing on nodes, topics, services, and `rclpy` for control.
      </>
    ),
  },
  {
    title: 'Module 2: The Digital Twin (Gazebo & Unity)',
    to: '/docs/02-gazebo-unity',
    description: (
      <>
        Dive into simulation environments, learning about physics, sensors (LiDAR, depth, IMU), and human-robot interaction in Unity.
      </>
    ),
  },
  {
    title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
    to: '/docs/03-isaac',
    description: (
      <>
        Understand NVIDIA Isaac Sim, Isaac ROS VSLAM, and `Nav2` for humanoid path planning.
      </>
    ),
  },
  {
    title: 'Module 4: Vision-Language-Action (VLA)',
    to: '/docs/04-vla',
    description: (
      <>
        Discover how voice commands (`Whisper`) and large language models (LLM) translate into robotic actions.
      </>
    ),
  },
  {
    title: 'Module 5: Capstone: The Autonomous Humanoid',
    to: '/docs/05-capstone',
    description: (
      <>
        Integrate concepts into an end-to-end autonomous humanoid system, covering voice, planning, navigation, perception, and manipulation.
      </>
    ),
  },
  {
    title: 'Module 6: References, Glossary & Further Reading',
    to: '/docs/06-references',
    description: (
      <>
        A curated list of resources, key terms, and suggestions for advanced study.
      </>
    ),
  },
];

function Feature({title, description, to}: FeatureItem) {
  return (
    <div className={clsx('col col--4 margin-bottom--lg')}>
      <div className="card">
        <div className="card__header">
          <Heading as="h3">{title}</Heading>
        </div>
        <div className="card__body">
          <p>{description}</p>
        </div>
        <div className="card__footer">
          <Link
            className="button button--primary button--block"
            to={to}>
            Read More
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

