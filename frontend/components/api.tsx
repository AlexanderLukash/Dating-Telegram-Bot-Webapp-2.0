import { BackEnd_URL } from "@/config/url";

// @ts-ignore
export async function getUserLike(from_user, to_user) {
    try {
        const res = await fetch(`https://4632-194-213-120-6.ngrok-free.app/api/v1/likes/${from_user}/${to_user}`, {
            method: 'GET',
            headers: {
                'bypass-tunnel-reminder': 'true',
                'User-Agent': 'Custom',
                'ngrok-skip-browser-warning': 'true'
            }
        });

        if (!res.ok) {
            throw new Error('Failed to fetch data');
        }

        const data = await res.json();

        // Перевіряємо та повертаємо статус лайка (true чи false)
        return data.status;
    } catch (error) {
        console.error('Помилка при перевірці лайка:', error);
        return false; // За замовчуванням повертаємо false у разі помилки
    }
}
