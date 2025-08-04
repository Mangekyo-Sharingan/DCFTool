import React, { useEffect, useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { CheckCircle, XCircle, AlertCircle, X, Info } from 'lucide-react';
import { cn } from '@/lib/utils';

interface NotificationState {
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  isVisible: boolean;
}

const NotificationBar: React.FC = () => {
  const [notification, setNotification] = useState<NotificationState>({
    type: 'info',
    message: '',
    isVisible: false
  });

  useEffect(() => {
    const handleShowNotification = (event: CustomEvent) => {
      const { type, message } = event.detail;
      setNotification({
        type,
        message,
        isVisible: true
      });
    };

    window.addEventListener('showNotification', handleShowNotification as EventListener);

    return () => {
      window.removeEventListener('showNotification', handleShowNotification as EventListener);
    };
  }, []);

  useEffect(() => {
    if (notification.isVisible) {
      const timer = setTimeout(() => {
        setNotification(prev => ({ ...prev, isVisible: false }));
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [notification.isVisible]);

  const onClose = () => {
    setNotification(prev => ({ ...prev, isVisible: false }));
  };

  const getIcon = () => {
    switch (notification.type) {
      case 'success':
        return <CheckCircle className="h-5 w-5" />;
      case 'error':
        return <XCircle className="h-5 w-5" />;
      case 'warning':
        return <AlertCircle className="h-5 w-5" />;
      case 'info':
        return <Info className="h-5 w-5" />;
      default:
        return <AlertCircle className="h-5 w-5" />;
    }
  };

  const getColorClasses = () => {
    switch (notification.type) {
      case 'success':
        return 'bg-green-500 border-green-600 text-white shadow-lg';
      case 'error':
        return 'bg-red-500 border-red-600 text-white shadow-lg';
      case 'warning':
        return 'bg-yellow-500 border-yellow-600 text-white shadow-lg';
      case 'info':
        return 'bg-blue-500 border-blue-600 text-white shadow-lg';
      default:
        return 'bg-blue-500 border-blue-600 text-white shadow-lg';
    }
  };

  if (!notification.isVisible) return null;

  return (
    <div className={cn(
      "fixed top-0 left-0 w-full z-50 transform transition-transform duration-300 ease-in-out",
      notification.isVisible ? "translate-y-0" : "-translate-y-full"
    )}>
      <div className={cn(
        "mx-4 mt-4 rounded-lg border shadow-lg",
        getColorClasses()
      )}>
        <Alert className="border-0 bg-transparent">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {getIcon()}
              <AlertDescription className="font-medium">
                {notification.message}
              </AlertDescription>
            </div>
            <button
              onClick={onClose}
              className="ml-4 hover:opacity-70 transition-opacity"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </Alert>
      </div>
    </div>
  );
};

export default NotificationBar;
