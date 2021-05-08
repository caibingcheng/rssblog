import styles from '../styles/Home.module.css'

const Footer = () => (
    <footer className={styles.footer} id="bottom-footer">
        <div>
            <a href="https://travellings.now.sh/" target="_blank" rel="noopener" title="开往-友链接力">
                <img src="https://travellings.now.sh/assets/logo.gif" alt="开往-友链接力" width="80" />
            </a>
        </div>
        <div>
            <a href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app" target="_blank" rel="noopener noreferrer">
                <img src="/vercel.svg" alt="Vercel Logo" className={styles.logo} />
            </a>
        </div>
    </footer>
)

export default Footer