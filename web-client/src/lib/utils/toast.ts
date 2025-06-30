import { toast as sonnerToast } from "sonner";

interface ToastOptions {
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  duration?: number;
}

export const toast = {
  success: (message: string, options?: ToastOptions) => {
    return sonnerToast.success(message, {
      ...options,
      style: {
        background: "#f0fdf4",
        border: "1px solid #bbf7d0",
        color: "#166534",
        fontFamily: "var(--font-montserrat)",
      },
    });
  },

  error: (message: string, options?: ToastOptions) => {
    return sonnerToast.error(message, {
      ...options,
      style: {
        background: "#fef2f2",
        border: "1px solid #fecaca",
        color: "#dc2626",
        fontFamily: "var(--font-montserrat)",
      },
    });
  },

  warning: (message: string, options?: ToastOptions) => {
    return sonnerToast.warning(message, {
      ...options,
      style: {
        background: "#fffbeb",
        border: "1px solid #fed7aa",
        color: "#d97706",
        fontFamily: "var(--font-montserrat)",
      },
    });
  },

  info: (message: string, options?: ToastOptions) => {
    return sonnerToast.info(message, {
      ...options,
      style: {
        background: "#eff6ff",
        border: "1px solid #bfdbfe",
        color: "#2563eb",
        fontFamily: "var(--font-montserrat)",
      },
    });
  },

  loading: (message: string, options?: ToastOptions) => {
    return sonnerToast.loading(message, {
      ...options,
      style: {
        background: "#f8fafc",
        border: "1px solid #e2e8f0",
        color: "#475569",
        fontFamily: "var(--font-montserrat)",
      },
    });
  },

  promise: <T>(
    promise: Promise<T>,
    {
      loading,
      success,
      error,
    }: {
      loading: string;
      success: string | ((data: T) => string);
      error: string | ((error: any) => string);
    }
  ) => {
    return sonnerToast.promise(promise, {
      loading,
      success,
      error,
      style: {
        fontFamily: "var(--font-montserrat)",
      },
    });
  },
};
