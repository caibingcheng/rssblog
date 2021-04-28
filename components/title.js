import Link from 'next/link'
import styles from '../styles/Home.module.css'
import Menu from './menu'

const Title = () => (
    <div>
        <h1 className={styles.title}>RSSBlog</h1>
        <p className={styles.description}>A Site for Blog RSS.</p>
        <Menu />
    </div>
)

export default Title