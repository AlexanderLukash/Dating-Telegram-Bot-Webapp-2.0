import React from "react";
import {BackEnd_URL} from "@/config/url";
import {CardUser} from "@/components/card";
import {revalidateTag} from 'next/cache';

async function getUsers(user_id: number) {
    try {
        const res = await fetch(`${BackEnd_URL}/api/v1/users/best_result/${user_id}`, {
            method: 'GET',
            headers: {
                'bypass-tunnel-reminder': 'true',
                'User-Agent': 'Custom',
                'cache': 'no-store',
                'ngrok-skip-browser-warning': 'true',
                'Cache-Control': 'no-store, max-age=0'
            },
            cache: 'no-store'
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`Failed to fetch data: ${res.status} - ${errorText}`);
        }

        return res.json();
    } catch (error) {
        // @ts-ignore
        console.error("Error fetching data:", error.message);
        throw error;
    }
}

// @ts-ignore
export default async function UsersPage({params}) {

    // Отримуємо дані користувачів
    const usersData = await getUsers(params.users)

    // Перевіряємо чи є користувачі
    const users = usersData.items;

    if (users && users.length > 0) {
        return (
            <div>
                {users.map((user: any, index: any) => (
                    <CardUser key={index} index={index} param={params} user={user}/>
                ))}
            </div>
        );
    } else {
        return (
            <h1 className="mt-20 mb-6 text-large font-bold leading-none text-default-600">
                Unfortunately, we have not found the right people for you. Try changing your profile parameters...
            </h1>
        );
    }
}
