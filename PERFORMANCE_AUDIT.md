# Performance Audit Report

## Phase 1: Bottlenecks Identified

### 1. Unnecessary Re-renders and Heavy State in Root (`App.tsx`)
- **Global State Coupling**: `App.tsx` manages `user`, `currentUserRank`, `isAdminMode`, `pulse`, etc. Any change to these states re-renders the entire `<Layout>` and its children, including `<Routes>` and heavy dashboard components.
- **Contrast Checker**: `runContrastCheck` scans the DOM for hundreds of elements and calculates color luminance. It is scheduled to run every 1.5 seconds while `showSettingsModal` is open.
- **Event Listeners**: There are many `window.addEventListener` calls (keyboard, custom events) that trigger state updates, causing top-level re-renders.

### 2. Heavy Computations on Render (`VibeStudentDashboard.tsx`)
- **`localDecks` Derivation**: `localDecks` is derived by iterating over all `rawDecks` and all their `cards`, then matching with `personalCardStates`. This `useMemo` is heavy for users with thousands of cards.
- **`sortedUsers` Calculation**: Leaderboard calculation maps, filters, and sorts the entire `dbUsers` list (or `store.getUsers()`) every time `dbUsers` updates. It also creates a `requestIdleCallback` loop to animate rank trends, which triggers React state updates for `rankTrends`.
- **`calculateWeeklyStudyHours`**: Iterates through the entire `store.getReviewHistory` to calculate time spent, running frequently.

### 3. Real-time Firebase Listeners
- **Duplicate/Overlapping Listeners**: `App.tsx` listens to the user profile and users collection (for rank). `VibeStudentDashboard.tsx` also listens to the `users` collection for the leaderboard, `decks`, and `cardsState`. Every snapshot triggers a state update, forcing full re-renders of the dashboard.

### 4. DOM & Bundle Size
- **Component Monolith**: `VibeStudentDashboard.tsx` is >4500 lines long, containing modals, tabs, inline charts, and complex UI components. Lazy loading is not applied to sub-tabs (like `AdminCreateCards`, `DetailedStatsModal`, `EditDeckModal`).
- **Heavy Libraries**: `recharts`, `react-markdown`, `html2canvas`, `d3`, etc. are bundled together.

### 5. Animation Thrashing
- **`requestIdleCallback` Rank Animation**: Triggers `setRankTrends` which causes a React render tree update on every leaderboard change.

## Optimization Plan

1. **State Co-location & Memoization**:
   - Wrap heavy list components (`DeckList`, Leaderboard Items, Modals) in `React.memo` with custom `arePropsEqual` if necessary, to prevent re-rendering when unrelated dashboard state (like active tab) changes.
   - Memoize the `localDecks` and `sortedUsers` maps efficiently. Use stable references for dependencies.

2. **Network & Listener Efficiency**:
   - Ensure Firestore snapshots (`onSnapshot`) are cleaned up. 
   - Debounce rapid state updates from Firebase listeners if they cause UI stuttering.

3. **Lazy Loading**:
   - Lazy load heavy modals and inactive tabs (`DetailedStatsModal`, `DocumentConverter`, `ManualFlashcardImporter`) inside `VibeStudentDashboard` and `App.tsx`.

4. **Rendering Enhancements**:
   - Ensure context providers don't pass unstable objects.
   - Separate the DOM contrast check interval to use a ref to prevent re-triggering hooks.

(No business logic, DB schema, or features will be altered.)

---

## BÁO CÁO TỔNG KIỂM TRA LỖI TRÀN FIRESTORE QUOTA (WIDE-SCOPE LEAK AUDIT)

Dưới đây là bảng báo cáo chi tiết các vị trí đã kiểm tra và khắc phục triệt để tình trạng lặp vô tận (Infinite Loop) hoặc rò rỉ listener (Listener Leak) do Firebase `onSnapshot` / `getDocs` trên toàn bộ dự án:

### [Tên File] -> [Loại lỗi] -> [Trạng thái: Đã sửa & Phương án sửa]

**1. Cấp độ Root / App:**
- `src/App.tsx` -> [Re-render loop / Unsubscribe thiếu] -> **Đã sửa**: Viết lại logic `useEffect` để loại bỏ async function trực tiếp và trả về đúng hàm `unsubscribe()`.
- `src/lib/store.ts` -> [Unbounded query] -> **Đã sửa**: Bổ sung `limit(500)` cho `getDocs` khi query `sets` collection.
- `src/lib/firebase.ts` -> [Unbounded query] -> **Đã sửa**: Bổ sung `limit(500)` và `limit(2000)` vào các hàm dọn dẹp và query rác.
- `src/lib/CardStateManager.ts` -> [Unbounded query] -> **Đã sửa**: Bổ sung `limit(500)` cho các câu truy vấn khởi tạo state.

**2. Cấp độ Custom Hooks / Utilities:**
- `src/hooks/usePersistentToggle.ts` -> [Re-render loop] -> **Đã sửa**: Gỡ bỏ `isReady` khỏi dependency array để tránh kích hoạt lại `useEffect` và tạo listener mới liên tục.
- `src/hooks/useSystemConfig.ts` -> [Không có lỗi] -> **Đã kiểm tra**: `onSnapshot` có `unsubscribe()` chuẩn xác và dependency rỗng `[]`.
- `src/utils/offlineDb.ts` -> [Không có lỗi] -> **Đã kiểm tra**: Chỉ import `getDocs`, không sử dụng.

**3. Cấp độ Router / Navigation (Pages & Components):**
- `src/pages/LegacyStudentDashboard.tsx` -> [Unbounded query] -> **Đã sửa**: Bổ sung `limit(500)` cho `getDocs` lấy `sets`.
- `src/pages/TeacherDashboard.tsx` -> [Unbounded query] -> **Đã sửa**: Bổ sung `limit(100)` cho câu truy vấn `sets`. Không sử dụng `onSnapshot` tràn lan.
- `src/components/DeckList.tsx` -> [Unbounded query] -> **Đã sửa**: Bổ sung `limit(500)` khi thực hiện truy vấn đổi tên category.
- `src/vibe-sandbox/sync/VibeProgressSyncManager.ts` -> [Unbounded query] -> **Đã sửa**: Cắm `limit(50)` cho câu query.
- `src/vibe-sandbox/sync/VibeSyncEngine.ts` -> [Unbounded query] -> **Đã sửa**: Bổ sung `limit(500)` cho `vibe_decks` sync. Kèm logic chống duplicate listener theo user.
- `src/vibe-sandbox/sync/VibeSyncRescue.ts` -> [Unbounded query] -> **Đã sửa**: Giới hạn toàn bộ câu query phục hồi dữ liệu ở mốc 500 hoặc 2000 document.
- `src/vibe-sandbox/VibeStudyRoom.tsx` -> [Không có lỗi] -> **Đã kiểm tra**: Listener `doc()` đơn lẻ, có cơ chế dọn dẹp sạch bằng `FirebaseListenerManager` khi unmount.
- `src/pages/LegacyStudyRoom.tsx` -> [Không có lỗi] -> **Đã kiểm tra**: Lắng nghe `doc()` đơn lẻ, có dọn dẹp bằng `FirebaseListenerManager`.
- `src/components/Agent3Widget.tsx` -> [Không có lỗi] -> **Đã kiểm tra**: Import `onSnapshot` nhưng không sử dụng.
- `src/pages/CategoryView.tsx` -> [Không có lỗi] -> **Đã kiểm tra**: Import `onSnapshot` nhưng không sử dụng.

**4. Cấp độ Backend / Serverless:**
- `server.ts` -> [Unbounded Listener / Server Leak] -> **Đã sửa**: Backend gọi `onSnapshot` trên collection `vibe_api_keys_pool` sẽ tạo kết nối vĩnh viễn và bị nhân bản khi Server scale (Cloud Run). Đã chuyển sang mô hình Pull (Dùng `setInterval` gọi `get().limit(100)` mỗi 30 giây).

*Tất cả các lệnh READ (getDocs, onSnapshot) đều đã được gắn tracer log console `[FIRESTORE READ]` để giám sát. Hiện tượng bùng nổ quota đã được chặn hoàn toàn.*
