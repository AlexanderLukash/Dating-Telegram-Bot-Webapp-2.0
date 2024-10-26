'use client';
import React, { useEffect, useState } from "react";
import { Button } from "@nextui-org/button";
import { HeartIconFill } from "@/components/HeartIconFill";
import { HeartIcon } from "@/components/HeartIcon";
import { getUserLike } from "@/components/api";
import { Spinner } from "@nextui-org/spinner";

export const LikeButton = ({ from_user_id, to_user_id }) => {
    const [liked, setLiked] = useState(false);
    const [showSpinner, setShowSpinner] = useState(true);

    // Отримання стану лайка при першому завантаженні
    useEffect(() => {
        const fetchLikeStatus = async () => {
            setShowSpinner(true); // Показуємо спіннер під час запиту
            try {
                const status = await getUserLike(from_user_id, to_user_id);
                setLiked(status); // Встановлюємо стан на основі отриманого статусу
            } catch (error) {
                console.error('Помилка при отриманні стану лайка:', error);
            }
            setShowSpinner(false); // Приховуємо спіннер після отримання статусу
        };
        fetchLikeStatus();
    }, [from_user_id, to_user_id]);

    const handleLikeClick = async () => {
        const updatedLiked = !liked;
        setLiked(updatedLiked);

        try {
            const response = await fetch(`https://4632-194-213-120-6.ngrok-free.app/api/v1/likes/`, {
                method: updatedLiked ? 'POST' : 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'bypass-tunnel-reminder': 'true',
                    'User-Agent': 'Custom',
                    'ngrok-skip-browser-warning': 'true'
                },
                body: JSON.stringify({
                    from_user: from_user_id,
                    to_user: to_user_id
                })
            });

            if (!response.ok) {
                throw new Error('Помилка при зміні стану лайка');
            }
        } catch (error) {
            console.error('Помилка при оновленні стану лайка:', error);
            setLiked(!updatedLiked); // Відміняємо зміну стану у разі помилки
        }
    };

    return (
        <>
            {showSpinner ? (
                <Spinner color="danger" size="sm" labelColor="danger" />
            ) : (
                <Button
                    isIconOnly
                    color="danger"
                    variant="faded"
                    aria-label="Like"
                    className="float-right"
                    onClick={handleLikeClick}
                >
                    {liked ? <HeartIconFill /> : <HeartIcon />}
                </Button>
            )}
        </>
    );
};