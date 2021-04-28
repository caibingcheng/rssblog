import Link from 'next/link'
import styles from '../styles/Home.module.css'

const Menu = () => (
    <div className={styles.menu}>
        <Link href="/">
            <a className={styles.menuhome, styles.normalink}>Home</a>
        </Link>
        &nbsp;|&nbsp;
        <Link href="/member">
            <a className={styles.menumember, styles.normalink}>Member</a>
        </Link>
    </div>
)

export default Menu